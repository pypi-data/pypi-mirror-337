#!/usr/bin/env python3
"""
Test Module for Table Storage Client
-----------------------------------
A modified version of the TableStorageClient for testing purposes.
This version imports SasTokenGenerator directly without package structure.
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

# Import SasTokenGenerator directly for testing
import sys
import importlib.util

current_dir = os.path.dirname(os.path.abspath(__file__))
api_keys_dir = os.path.dirname(current_dir)
module_path = os.path.join(api_keys_dir, "services", "sas_token_generator.py")

# Import using importlib for testing
spec = importlib.util.spec_from_file_location("sas_token_generator", module_path)
sas_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sas_module)
SasTokenGenerator = sas_module.SasTokenGenerator

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
            self.sas_generator = SasTokenGenerator(
                connection_string=self.connection_string
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
            self.sas_token = self.sas_generator.generate_table_sas(
                expiry_hours=24,  # 24 hour token by default
                permissions="raud"  # read, add, update, delete
            )
            if not self.endpoint and self.sas_generator:
                self.endpoint = self.sas_generator.get_account_endpoint("table")
            
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
"""
Test Module for Table Storage Client
-----------------------------------
A modified version of the TableStorageClient for testing purposes.
This version imports SasTokenGenerator directly without package structure.
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

# Import SasTokenGenerator directly for testing
import sys
import importlib.util

current_dir = os.path.dirname(os.path.abspath(__file__))
api_keys_dir = os.path.dirname(current_dir)
module_path = os.path.join(api_keys_dir, "services", "sas_token_generator.py")

# Import using importlib for testing
spec = importlib.util.spec_from_file_location("sas_token_generator", module_path)
sas_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sas_module)
SasTokenGenerator = sas_module.SasTokenGenerator

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
            self.sas_generator = SasTokenGenerator(
                connection_string=self.connection_string
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
            self.sas_token = self.sas_generator.generate_table_sas(
                expiry_hours=24,  # 24 hour token by default
                permissions="raud"  # read, add, update, delete
            )
            if not self.endpoint and self.sas_generator:
                self.endpoint = self.sas_generator.get_account_endpoint("table")
            
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