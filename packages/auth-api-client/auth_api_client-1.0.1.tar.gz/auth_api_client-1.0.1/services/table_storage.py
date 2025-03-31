"""
Azure Table Storage Service
--------------------------
A modular service for interacting with Azure Table Storage.
This provides a clean interface for CRUD operations on tables.
"""

import logging
import os
import json
import urllib.request
import urllib.parse
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
from functools import wraps

from azure.data.tables import TableServiceClient, TableClient, UpdateMode
from azure.core.credentials import AzureSasCredential
from azure.core.exceptions import ResourceExistsError, HttpResponseError

from api_keys.services.sas_token_generator import SasTokenGenerator

# Configure logging
logger = logging.getLogger(__name__)

class TableStorageClient:
    """Modular client for Azure Table Storage operations."""
    
    def __init__(self, 
                connection_string: Optional[str] = None, 
                table_names: Optional[List[str]] = None,
                endpoint: Optional[str] = None,
                sas_token: Optional[str] = None,
                use_sas_generator: bool = False):
        """Initialize the Table Storage client.
        
        Args:
            connection_string: Azure Storage connection string
            table_names: List of table names to initialize
            endpoint: Azure Table storage endpoint URL (used with SAS token)
            sas_token: SAS token for authentication (instead of connection string)
            use_sas_generator: Whether to use external SAS token generator
        """
        self.connection_string = connection_string or os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.endpoint = endpoint or os.getenv("AZURE_STORAGE_ENDPOINT")
        self.sas_token = sas_token or os.getenv("AZURE_STORAGE_SAS_TOKEN")
        self.use_sas_generator = use_sas_generator
        
        # SAS token generator
        self.sas_generator = None
        if use_sas_generator:
            # Use the same pattern we validated in tests - providing account_name with connection_string
            account_name = None
            # Try to extract account name from connection string if available
            if self.connection_string:
                try:
                    parts = self.connection_string.split(';')
                    for part in parts:
                        if part.startswith('AccountName='):
                            account_name = part.split('=', 1)[1]
                            break
                except Exception:
                    pass
            
            self.sas_generator = SasTokenGenerator(
                connection_string=self.connection_string,
                account_name=account_name or os.getenv("AZURE_STORAGE_ACCOUNT")
            )
        
        self.table_service = None
        self.tables = {}  # Dictionary of table clients
        self._initialized = False
        self.table_names = table_names or []
        
    def initialize(self) -> bool:
        """Initialize connection to Azure Table Storage.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self._initialized:
            return True
            
        # Try to generate SAS token if requested
        if self.use_sas_generator and not self.sas_token and self.sas_generator:
            try:
                # Generate SAS token with fallback capability
                self.sas_token = self.sas_generator.generate_table_sas(
                    expiry_hours=24,  # 24 hour token by default
                    permissions="raud",  # read, add, update, delete
                    table_name=None  # Access to all tables
                )
                
                # If token generation failed due to rate limiting or other issues, log it
                if not self.sas_token:
                    logger.warning("Failed to generate SAS token - may be rate limited or service unavailable")
                    # Continue with other authentication methods
                else:
                    logger.info("Successfully generated SAS token for table access")
                    
                # Get the endpoint if not already specified
                if not self.endpoint and self.sas_generator:
                    self.endpoint = self.sas_generator.get_account_endpoint("table")
                    if self.endpoint:
                        logger.info(f"Using endpoint: {self.endpoint}")
                    else:
                        logger.warning("Failed to determine table storage endpoint")
            except Exception as e:
                logger.error(f"Error generating SAS token: {str(e)}")
                # Continue with other authentication methods
        
        # Determine authentication method
        if not (self.connection_string or (self.endpoint and self.sas_token)):
            logger.error("No Azure Storage connection details provided")
            return False
            
        try:
            logger.info("Initializing Azure Table Storage")
            
            # Use SAS token if available
            if self.endpoint and self.sas_token:
                logger.info("Using SAS token authentication")
                credential = AzureSasCredential(self.sas_token)
                self.table_service = TableServiceClient(
                    endpoint=self.endpoint,
                    credential=credential
                )
            # Fall back to connection string
            elif self.connection_string:
                logger.info("Using connection string authentication")
                self.table_service = TableServiceClient.from_connection_string(
                    conn_str=self.connection_string
                )
            else:
                logger.error("No valid authentication method available")
                return False
            
            # Create tables if they don't exist
            for table_name in self.table_names:
                self._ensure_table_exists(table_name)
                
            self._initialized = True
            logger.info("Azure Table Storage initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Azure Table Storage: {str(e)}")
            return False
    
    def _ensure_table_exists(self, table_name: str) -> bool:
        """Create table if it doesn't exist.
        
        Args:
            table_name: Name of the table to create
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.table_service:
            return False
            
        try:
            self.table_service.create_table(table_name)
            logger.info(f"Created table {table_name}")
        except ResourceExistsError:
            logger.info(f"Table {table_name} already exists")
        except Exception as e:
            logger.error(f"Failed to create table {table_name}: {str(e)}")
            return False
            
        # Get table client
        self.tables[table_name] = self.table_service.get_table_client(table_name)
        return True
    
    def get_table_client(self, table_name: str) -> Optional[TableClient]:
        """Get a table client for the specified table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            TableClient or None if table doesn't exist or client not initialized
        """
        if table_name not in self.tables:
            if not self._ensure_table_exists(table_name):
                return None
        
        return self.tables.get(table_name)
    
    def create_entity(self, table_name: str, entity: Dict[str, Any]) -> bool:
        """Create a new entity in the specified table.
        
        Args:
            table_name: Name of the table
            entity: Entity data (must contain PartitionKey and RowKey)
            
        Returns:
            bool: True if successful, False otherwise
        """
        table = self.get_table_client(table_name)
        if not table:
            return False
            
        try:
            table.create_entity(entity=entity)
            return True
        except Exception as e:
            logger.error(f"Failed to create entity in {table_name}: {str(e)}")
            return False
    
    def update_entity(self, 
                     table_name: str, 
                     entity: Dict[str, Any], 
                     mode: UpdateMode = UpdateMode.MERGE) -> bool:
        """Update an existing entity in the specified table.
        
        Args:
            table_name: Name of the table
            entity: Entity data (must contain PartitionKey and RowKey)
            mode: Update mode (MERGE or REPLACE)
            
        Returns:
            bool: True if successful, False otherwise
        """
        table = self.get_table_client(table_name)
        if not table:
            return False
            
        try:
            table.update_entity(entity=entity, mode=mode)
            return True
        except Exception as e:
            logger.error(f"Failed to update entity in {table_name}: {str(e)}")
            return False
    
    def get_entity(self, 
                  table_name: str, 
                  partition_key: str, 
                  row_key: str) -> Optional[Dict[str, Any]]:
        """Get an entity from the specified table.
        
        Args:
            table_name: Name of the table
            partition_key: Partition key of the entity
            row_key: Row key of the entity
            
        Returns:
            Dict or None if entity doesn't exist or error occurs
        """
        table = self.get_table_client(table_name)
        if not table:
            return None
            
        try:
            return table.get_entity(partition_key=partition_key, row_key=row_key)
        except HttpResponseError as e:
            if e.status_code == 404:
                logger.info(f"Entity not found in {table_name}: {partition_key}/{row_key}")
            else:
                logger.error(f"Failed to get entity from {table_name}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Failed to get entity from {table_name}: {str(e)}")
            return None
    
    def delete_entity(self, 
                     table_name: str, 
                     partition_key: str, 
                     row_key: str) -> bool:
        """Delete an entity from the specified table.
        
        Args:
            table_name: Name of the table
            partition_key: Partition key of the entity
            row_key: Row key of the entity
            
        Returns:
            bool: True if successful, False otherwise
        """
        table = self.get_table_client(table_name)
        if not table:
            return False
            
        try:
            table.delete_entity(partition_key=partition_key, row_key=row_key)
            return True
        except Exception as e:
            logger.error(f"Failed to delete entity from {table_name}: {str(e)}")
            return False
    
    def query_entities(self, 
                      table_name: str, 
                      query_filter: Optional[str] = None,
                      select: Optional[str] = None) -> List[Dict[str, Any]]:
        """Query entities from the specified table.
        
        Args:
            table_name: Name of the table
            query_filter: OData filter query
            select: Comma-separated list of properties to return
            
        Returns:
            List of entities matching the query
        """
        table = self.get_table_client(table_name)
        if not table:
            return []
            
        try:
            query_params = {}
            if query_filter:
                query_params['filter'] = query_filter
            if select:
                query_params['select'] = select.split(',')
                
            return list(table.query_entities(**query_params))
        except Exception as e:
            logger.error(f"Failed to query entities from {table_name}: {str(e)}")
            return []
            
    def upsert_entity(self, table_name: str, entity: Dict[str, Any]) -> bool:
        """Create or update an entity in the specified table.
        
        Args:
            table_name: Name of the table
            entity: Entity data (must contain PartitionKey and RowKey)
            
        Returns:
            bool: True if successful, False otherwise
        """
        table = self.get_table_client(table_name)
        if not table:
            return False
            
        try:
            table.upsert_entity(entity=entity)
            return True
        except Exception as e:
            logger.error(f"Failed to upsert entity in {table_name}: {str(e)}")
            return False 