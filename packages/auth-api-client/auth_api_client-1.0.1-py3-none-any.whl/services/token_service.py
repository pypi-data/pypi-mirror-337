"""
Token Service - Dedicated service for token management.
This service encapsulates the logic for creating, validating, and managing tokens.
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple
from uuid import uuid4
import logging
import os
import hashlib
import secrets
import string
import json
import sqlite3
from pathlib import Path
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as cosmos_exceptions
from azure.cosmos.partition_key import PartitionKey
from azure.data.tables import UpdateMode
from azure.core.exceptions import ResourceExistsError, HttpResponseError
import asyncio
from functools import wraps
import time
import contextlib

# Import our modular Table Storage client
from api_keys.services.table_storage import TableStorageClient

# Constants
API_KEYS_TABLE = "APIKeys"
API_KEY_USAGE_TABLE = "APIKeyUsage"
PROVIDER_PARTITION_KEY = "PROVIDER"
USAGE_PARTITION_KEY = "USAGE"

# Configure verbose logging
logger = logging.getLogger(__name__)

@contextlib.contextmanager
def transaction_scope(conn):
    """Transaction context manager.
    
    This ensures that a connection is always properly committed or
    rolled back and closed regardless of whether an exception occurs.
    """
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def with_circuit_breaker(max_retries=3, cooldown_seconds=5):
    """Circuit breaker decorator for Cosmos DB operations."""
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return await func(self, *args, **kwargs)
                except cosmos_exceptions.CosmosHttpResponseError as e:
                    if e.status_code == 429:  # Too Many Requests
                        # Get retry after duration from headers or use default
                        retry_after = int(e.http_headers.get('x-ms-retry-after-ms', cooldown_seconds * 1000) / 1000)
                        logger.warning(f"Rate limited by Cosmos DB, waiting {retry_after} seconds")
                        await asyncio.sleep(retry_after)
                        retries += 1
                        continue
                    raise
                except Exception as e:
                    logger.error(f"Cosmos DB operation failed: {str(e)}")
                    if not self._fallback_mode:
                        self._fallback_mode = True
                        logger.info("Switching to fallback mode")
                    raise
            return await func(self, *args, **kwargs)
        return wrapper
    return decorator

class TokenService:
    """Service for token management"""
    
    def __init__(self, connection_string=None):
        """Initialize token service."""
        self._initialized = False
        self._fallback_mode = os.getenv("DB_FALLBACK", "true").lower() == "true"
        self.logger = logger
        self.connection_string = connection_string or os.getenv("AZURE_COSMODB_CONNECTION_STRING")
        self.db_path = os.getenv("DB_PATH", "/data/api_keys.db")
        self.cosmos_db = None
        self.cosmos_container = None
        self.cosmos_usage_container = None
        self._cosmos_ru_limit = int(os.getenv("COSMOS_RU_LIMIT", "400"))
        self._cosmos_batch_size = int(os.getenv("COSMOS_BATCH_SIZE", "100"))
        
        # Azure Table Storage
        self.use_table_storage = os.getenv("USE_AZURE_TABLE_STORAGE", "false").lower() == "true"
        self.table_connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        
        # Initialize our modular Table Storage client
        self.table_storage = None
        
    @with_circuit_breaker()
    async def init(self):
        """Initialize the service."""
        if self._initialized:
            return
        
        # Initialize Azure Table Storage if enabled
        if self.use_table_storage and (self.table_connection_string or os.getenv("AZURE_STORAGE_ENDPOINT")):
            try:
                self.logger.info("Initializing Azure Table Storage")
                
                # Check if we should use SAS token generator
                use_sas_generator = os.getenv("USE_AZURE_SAS_GENERATOR", "false").lower() == "true"
                table_endpoint = os.getenv("AZURE_STORAGE_ENDPOINT")
                table_sas_token = os.getenv("AZURE_STORAGE_SAS_TOKEN")
                
                # Use our modular TableStorageClient with appropriate authentication
                self.table_storage = TableStorageClient(
                    connection_string=self.table_connection_string, 
                    table_names=[API_KEYS_TABLE, API_KEY_USAGE_TABLE],
                    endpoint=table_endpoint,
                    sas_token=table_sas_token,
                    use_sas_generator=use_sas_generator
                )
                
                # Initialize the client and create tables
                if self.table_storage.initialize():
                    self.logger.info("Azure Table Storage initialized successfully")
                else:
                    self.logger.error("Failed to initialize Azure Table Storage")
                    self.use_table_storage = False
                    # Fall back to SQLite
            except Exception as e:
                self.logger.error(f"Failed to initialize Azure Table Storage: {str(e)}")
                self.use_table_storage = False
                # Fall back to SQLite
            
        # Always initialize SQLite for fallback
        if not self.use_table_storage:
            self.db_path = self._get_db_path()
            conn = self._get_db_connection()
            c = conn.cursor()
            
            # Create API Keys table
            c.execute('''
                CREATE TABLE IF NOT EXISTS APIKeys (
                    id TEXT PRIMARY KEY,
                    provider_id TEXT,
                    name TEXT,
                    token_hash TEXT,
                    scopes TEXT,
                    status TEXT,
                    created_at TEXT,
                    expires_at TEXT,
                    description TEXT,
                    ip_restrictions TEXT,
                    is_revoked INTEGER,
                    revoked_at TEXT,
                    revocation_reason TEXT,
                    last_used_at TEXT,
                    environment TEXT,
                    metadata TEXT,
                    synced_to_cosmos INTEGER DEFAULT 0
                )
            ''')
            
            # Create API Key Usage table
            c.execute('''
                CREATE TABLE IF NOT EXISTS APIKeyUsage (
                    token_id TEXT PRIMARY KEY,
                    request_count INTEGER,
                    last_used TEXT,
                    endpoints TEXT,
                    status_codes TEXT,
                    errors TEXT,
                    synced_to_cosmos INTEGER DEFAULT 0
                )
            ''')
            
            conn.commit()
            conn.close()

        # Try to initialize Cosmos DB if not in fallback mode
        if not self._fallback_mode and self.connection_string:
            try:
                client = cosmos_client.CosmosClient.from_connection_string(
                    self.connection_string,
                    retry_total=3,
                    retry_backoff_max=15
                )
                database_name = os.getenv("AZURE_COSMODB_DATABASE", "api_keys")
                
                # Create database if it doesn't exist
                self.cosmos_db = client.create_database_if_not_exists(id=database_name)
                
                # Create containers if they don't exist with traffic control settings
                self.cosmos_container = self.cosmos_db.create_container_if_not_exists(
                    id=API_KEYS_TABLE,
                    partition_key=PartitionKey(path="/provider_id"),
                    offer_throughput=self._cosmos_ru_limit
                )
                
                self.cosmos_usage_container = self.cosmos_db.create_container_if_not_exists(
                    id=API_KEY_USAGE_TABLE,
                    partition_key=PartitionKey(path="/token_id"),
                    offer_throughput=self._cosmos_ru_limit
                )
                
                # Sync any unsynced records from SQLite to Cosmos in batches
                if not self.use_table_storage:
                    await self._sync_to_cosmos()
                
            except Exception as e:
                self.logger.error(f"Failed to initialize Cosmos DB: {str(e)}")
                self._fallback_mode = True
        
        self._initialized = True
    
    @with_circuit_breaker()
    async def _sync_to_cosmos(self):
        """Sync unsynced records from SQLite to Cosmos DB in batches."""
        if self._fallback_mode or not self.cosmos_container:
            return
            
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Sync API Keys in batches
        c.execute("SELECT * FROM APIKeys WHERE synced_to_cosmos = 0")
        unsynced_keys = c.fetchall()
        
        for i in range(0, len(unsynced_keys), self._cosmos_batch_size):
            batch = unsynced_keys[i:i + self._cosmos_batch_size]
            
            for key in batch:
                try:
                    # Convert row to dict
                    columns = [desc[0] for desc in c.description]
                    key_dict = dict(zip(columns, key))
                    
                    # Remove sqlite-specific field
                    key_dict.pop('synced_to_cosmos', None)
                    
                    # Create in Cosmos with optimistic concurrency
                    self.cosmos_container.create_item(
                        body=key_dict,
                        enable_automatic_id_generation=False
                    )
                    
                    # Mark as synced
                    c.execute("UPDATE APIKeys SET synced_to_cosmos = 1 WHERE id = ?", (key_dict['id'],))
                    
                except cosmos_exceptions.CosmosResourceExistsError:
                    # Item already exists, mark as synced
                    c.execute("UPDATE APIKeys SET synced_to_cosmos = 1 WHERE id = ?", (key_dict['id'],))
                except Exception as e:
                    self.logger.error(f"Failed to sync key {key[0]} to Cosmos: {str(e)}")
            
            # Commit after each batch
            conn.commit()
            
            # Add a small delay between batches to control traffic
            await asyncio.sleep(0.1)
        
        # Sync Usage data in batches
        c.execute("SELECT * FROM APIKeyUsage WHERE synced_to_cosmos = 0")
        unsynced_usage = c.fetchall()
        
        for i in range(0, len(unsynced_usage), self._cosmos_batch_size):
            batch = unsynced_usage[i:i + self._cosmos_batch_size]
            
            for usage in batch:
                try:
                    columns = [desc[0] for desc in c.description]
                    usage_dict = dict(zip(columns, usage))
                    usage_dict.pop('synced_to_cosmos', None)
                    usage_dict['id'] = usage_dict['token_id']  # Add required id field
                    
                    self.cosmos_usage_container.create_item(
                        body=usage_dict,
                        enable_automatic_id_generation=False
                    )
                    
                    c.execute("UPDATE APIKeyUsage SET synced_to_cosmos = 1 WHERE token_id = ?", (usage_dict['token_id'],))
                    
                except cosmos_exceptions.CosmosResourceExistsError:
                    c.execute("UPDATE APIKeyUsage SET synced_to_cosmos = 1 WHERE token_id = ?", (usage_dict['token_id'],))
                except Exception as e:
                    self.logger.error(f"Failed to sync usage for token {usage[0]} to Cosmos: {str(e)}")
            
            # Commit after each batch
            conn.commit()
            
            # Add a small delay between batches
            await asyncio.sleep(0.1)
        
        conn.close()
    
    def _generate_token(self, environment: str) -> str:
        """Generate a secure token."""
        chars = string.ascii_letters + string.digits
        random_part = ''.join(secrets.choice(chars) for _ in range(32))
        return f"permas_{environment}_{random_part}"
    
    async def create_token(
        self, 
        provider_id: str, 
        name: str, 
        scopes: List[str],
        environment: str = "test",
        expires_in_days: Optional[int] = 365,
        description: Optional[str] = None,
        ip_restrictions: Optional[List[str]] = None
    ) -> Tuple[Dict[str, Any], str]:
        """Create a new API token."""
        await self.init()
        
        # Generate token data
        raw_token = self._generate_token(environment)
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        token_id = str(uuid4())
        now = datetime.utcnow()
        expires_at = now + timedelta(days=expires_in_days) if expires_in_days else None
        
        token_data = {
            "id": token_id,
            "provider_id": provider_id,
            "name": name,
            "token_hash": token_hash,
            "scopes": ",".join(scopes),
            "status": "active",
            "created_at": now.isoformat(),
            "expires_at": expires_at.isoformat() if expires_at else None,
            "description": description or f"API key for {name}",
            "ip_restrictions": ",".join(ip_restrictions) if ip_restrictions else "",
            "is_revoked": False,
            "revoked_at": None,
            "revocation_reason": None,
            "last_used_at": None,
            "environment": environment,
            "metadata": "{}"
        }
        
        # If Azure Table Storage is enabled
        if self.use_table_storage and self.table_storage:
            try:
                # Prepare entity for Table Storage
                # Table Storage requires PartitionKey and RowKey
                entity = {
                    "PartitionKey": provider_id,
                    "RowKey": token_id,
                    **token_data  # Include all other fields
                }
                
                # Create token entity using our modular client
                success = self.table_storage.create_entity(API_KEYS_TABLE, entity)
                
                if not success:
                    raise Exception("Failed to create token entity")
                
                # Create usage tracking entity
                usage_entity = {
                    "PartitionKey": token_id,
                    "RowKey": token_id,
                    "token_id": token_id,
                    "request_count": 0,
                    "last_used": None,
                    "endpoints": "{}",
                    "status_codes": "{}",
                    "errors": "[]"
                }
                success = self.table_storage.create_entity(API_KEY_USAGE_TABLE, usage_entity)
                
                if not success:
                    raise Exception("Failed to create usage entity")
                
                self.logger.info(f"Created token {token_id} for provider {provider_id} in Azure Table Storage")
                return token_data, raw_token
                
            except Exception as e:
                self.logger.error(f"Failed to create token in Azure Table Storage: {str(e)}")
                # Fall back to SQLite
        
        # Otherwise use SQLite
        conn = self._get_db_connection()
        
        try:
            with transaction_scope(conn) as cursor:
                placeholders = ", ".join(["?"] * len(token_data))
                columns = ", ".join(token_data.keys())
                values = list(token_data.values())
                
                cursor.execute(f"INSERT INTO APIKeys ({columns}) VALUES ({placeholders})", values)
                
                # Initialize usage tracking
                cursor.execute(
                    "INSERT INTO APIKeyUsage (token_id, request_count, last_used, endpoints, status_codes, errors) VALUES (?, ?, ?, ?, ?, ?)",
                    [token_id, 0, None, "{}", "{}", "[]"]
                )
        except Exception as e:
            self.logger.error(f"Failed to create token in SQLite: {str(e)}")
            raise
        
        # If not in fallback mode, try to save to Cosmos
        if not self._fallback_mode and self.cosmos_container:
            try:
                self.cosmos_container.create_item(body=token_data)
                self.cosmos_usage_container.create_item(body={
                    "id": token_id,
                    "token_id": token_id,
                    "request_count": 0,
                    "last_used": None,
                    "endpoints": "{}",
                    "status_codes": "{}",
                    "errors": "[]"
                })
                # Mark as synced in SQLite
                conn = self._get_db_connection()
                try:
                    with transaction_scope(conn) as cursor:
                        cursor.execute("UPDATE APIKeys SET synced_to_cosmos = 1 WHERE id = ?", (token_id,))
                        cursor.execute("UPDATE APIKeyUsage SET synced_to_cosmos = 1 WHERE token_id = ?", (token_id,))
                except Exception as e:
                    self.logger.error(f"Failed to mark token as synced: {str(e)}")
            except Exception as e:
                self.logger.error(f"Failed to save to Cosmos DB: {str(e)}")
                # Continue with SQLite only
                self._fallback_mode = True
        
        self.logger.info(f"Created token {token_id} for provider {provider_id}")
        return token_data, raw_token

    async def list_tokens(self, provider_id: str) -> List[Dict[str, Any]]:
        """List all tokens for a provider."""
        await self.init()
        
        # Try table storage if enabled
        if self.use_table_storage and self.table_storage:
            try:
                # Query for tokens with the given provider_id as PartitionKey
                query_filter = f"PartitionKey eq '{provider_id}'"
                tokens = self.table_storage.query_entities(API_KEYS_TABLE, query_filter)
                
                if tokens:
                    # Remove Table Storage specific fields
                    for token in tokens:
                        token.pop('PartitionKey', None)
                        token.pop('RowKey', None)
                        token.pop('odata.etag', None)
                        token.pop('Timestamp', None)
                    
                    return tokens
            except Exception as e:
                self.logger.error(f"Failed to query tokens from Table Storage: {str(e)}")
                # Fall back to other methods
            
        # Try Cosmos DB if available and not in fallback mode
        if not self._fallback_mode and self.cosmos_container:
            try:
                query = f"SELECT * FROM c WHERE c.provider_id = @provider_id"
                params = [{"name": "@provider_id", "value": provider_id}]
                items = list(self.cosmos_container.query_items(
                    query=query,
                    parameters=params,
                    enable_cross_partition_query=True
                ))
                if items:
                    return items
            except Exception as e:
                self.logger.error(f"Failed to query Cosmos DB: {str(e)}")
                self._fallback_mode = True
        
        # Fallback to SQLite
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("PRAGMA table_info(APIKeys)")
        columns = [column[1] for column in c.fetchall()]
        
        c.execute("SELECT * FROM APIKeys WHERE provider_id = ?", (provider_id,))
        tokens = c.fetchall()
        
        conn.close()
        
        return [dict(zip(columns, token)) for token in tokens]

    async def revoke_token(self, token_id: str, reason: str) -> Dict[str, Any]:
        """Revoke an API token."""
        await self.init()
        
        now = datetime.utcnow().isoformat()
        revocation_data = {
            "is_revoked": True,
            "revoked_at": now,
            "revocation_reason": reason,
            "status": "revoked"
        }
        
        # Try to update in Table Storage if enabled
        if self.use_table_storage and self.table_storage:
            try:
                # First get the token to find its PartitionKey (provider_id)
                # We need the partition key to uniquely identify the token
                token_entities = self.table_storage.query_entities(
                    API_KEYS_TABLE, 
                    f"RowKey eq '{token_id}'"
                )
                
                if token_entities:
                    token_entity = token_entities[0]
                    provider_id = token_entity.get("PartitionKey")
                    
                    # Build the update entity with both required keys
                    update_entity = {
                        "PartitionKey": provider_id,
                        "RowKey": token_id,
                        **revocation_data
                    }
                    
                    # Update the entity
                    success = self.table_storage.update_entity(API_KEYS_TABLE, update_entity)
                    
                    if success:
                        self.logger.info(f"Revoked token {token_id} in Table Storage")
                        revocation_data["id"] = token_id
                        return revocation_data
                else:
                    self.logger.warning(f"Token {token_id} not found in Table Storage")
            except Exception as e:
                self.logger.error(f"Failed to revoke token in Table Storage: {str(e)}")
        
        # Always update SQLite as fallback
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("SELECT * FROM APIKeys WHERE id = ?", (token_id,))
        token = c.fetchone()
        
        if not token:
            conn.close()
            raise ValueError(f"Token {token_id} not found")
        
        c.execute(
            "UPDATE APIKeys SET is_revoked = ?, revoked_at = ?, revocation_reason = ?, status = ? WHERE id = ?",
            [True, now, reason, "revoked", token_id]
        )
        
        # Try to update Cosmos if not in fallback mode
        if not self._fallback_mode and self.cosmos_container:
            try:
                # Get the token from Cosmos
                token_doc = self.cosmos_container.read_item(
                    item=token_id,
                    partition_key=token[1]  # provider_id from SQLite
                )
                
                # Update the token
                token_doc.update(revocation_data)
                self.cosmos_container.replace_item(
                    item=token_id,
                    body=token_doc
                )
                
                # Mark as synced in SQLite
                c.execute("UPDATE APIKeys SET synced_to_cosmos = 1 WHERE id = ?", (token_id,))
                
            except Exception as e:
                self.logger.error(f"Failed to update token in Cosmos DB: {str(e)}")
                self._fallback_mode = True
        
        conn.commit()
        conn.close()
        
        revocation_data["id"] = token_id
        return revocation_data
    
    async def _get_usage_from_sqlite(self, token_id: str) -> Optional[Dict[str, Any]]:
        """Get usage data from SQLite."""
        conn = sqlite3.connect(self.db_path)
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM APIKeyUsage WHERE token_id = ?", (token_id,))
            row = c.fetchone()
            
            if row:
                columns = [desc[0] for desc in c.description]
                usage_dict = dict(zip(columns, row))
                usage_dict.pop('synced_to_cosmos', None)  # Remove SQLite-specific field
                
                # Parse JSON fields
                usage_dict['endpoints'] = json.loads(usage_dict['endpoints']) if usage_dict['endpoints'] else {}
                usage_dict['status_codes'] = json.loads(usage_dict['status_codes']) if usage_dict['status_codes'] else {}
                usage_dict['errors'] = json.loads(usage_dict['errors']) if usage_dict['errors'] else []
                
                return usage_dict
            return None
        finally:
            conn.close()
            
    async def _get_usage_from_table_storage(self, token_id: str) -> Optional[Dict[str, Any]]:
        """Get usage data from Table Storage."""
        if not self.table_storage:
            return None
            
        try:
            # Query for the usage entity with token_id as both PartitionKey and RowKey
            entity = self.table_storage.get_entity(API_KEY_USAGE_TABLE, token_id, token_id)
            
            if entity:
                # Clean up the entity by removing Table Storage specific fields
                entity.pop('PartitionKey', None)
                entity.pop('RowKey', None)
                entity.pop('odata.etag', None)
                entity.pop('Timestamp', None)
                
                # Parse JSON fields
                entity['endpoints'] = json.loads(entity['endpoints']) if entity['endpoints'] else {}
                entity['status_codes'] = json.loads(entity['status_codes']) if entity['status_codes'] else {}
                entity['errors'] = json.loads(entity['errors']) if entity['errors'] else []
                
                return entity
        except Exception as e:
            self.logger.error(f"Failed to get usage from Table Storage: {str(e)}")
            
        return None

    @with_circuit_breaker()
    async def get_api_key_usage(self, token_id: str) -> Dict[str, Any]:
        """Get usage statistics for an API key."""
        await self.init()
        
        # First try Table Storage if enabled
        if self.use_table_storage and self.table_storage:
            usage = await self._get_usage_from_table_storage(token_id)
            if usage:
                return usage
        
        # Next try SQLite
        usage = await self._get_usage_from_sqlite(token_id)
        if usage:
            return usage
            
        # If not found in SQLite and Cosmos DB is available, try there
        if not self._fallback_mode and self.cosmos_usage_container:
            try:
                doc = self.cosmos_usage_container.read_item(item=token_id, partition_key=token_id)
                return {
                    'token_id': doc['token_id'],
                    'request_count': doc['request_count'],
                    'last_used': doc['last_used'],
                    'endpoints': doc['endpoints'],
                    'status_codes': doc['status_codes'],
                    'errors': doc['errors']
                }
            except cosmos_exceptions.CosmosResourceNotFoundError:
                pass
            except Exception as e:
                self.logger.error(f"Failed to get usage from Cosmos DB: {str(e)}")
        
        # If not found anywhere, return empty usage data
        return {
            'token_id': token_id,
            'request_count': 0,
            'last_used': None,
            'endpoints': {},
            'status_codes': {},
            'errors': []
        }
    
    async def log_token_usage(
        self, 
        token_id: str, 
        endpoint: str, 
        status_code: int,
        error: Optional[str] = None
    ) -> None:
        """Log token usage."""
        await self.init()
        
        now = datetime.utcnow().isoformat()
        
        # Try to update in Table Storage first if enabled
        if self.use_table_storage and self.table_storage:
            try:
                # First try to get existing entity
                entity = self.table_storage.get_entity(API_KEY_USAGE_TABLE, token_id, token_id)
                
                if entity:
                    # Update existing entity
                    # Parse JSON fields
                    endpoints = json.loads(entity.get('endpoints', '{}')) if entity.get('endpoints') else {}
                    endpoints[endpoint] = endpoints.get(endpoint, 0) + 1
                    
                    status_codes = json.loads(entity.get('status_codes', '{}')) if entity.get('status_codes') else {}
                    status_codes[str(status_code)] = status_codes.get(str(status_code), 0) + 1
                    
                    errors = json.loads(entity.get('errors', '[]')) if entity.get('errors') else []
                    if error:
                        errors.append({
                            "timestamp": now,
                            "endpoint": endpoint,
                            "error": error
                        })
                    
                    # Prepare updated entity
                    updated_entity = {
                        "PartitionKey": token_id,
                        "RowKey": token_id,
                        "request_count": entity.get('request_count', 0) + 1,
                        "last_used": now,
                        "endpoints": json.dumps(endpoints),
                        "status_codes": json.dumps(status_codes),
                        "errors": json.dumps(errors)
                    }
                    
                    success = self.table_storage.update_entity(API_KEY_USAGE_TABLE, updated_entity)
                    if success:
                        self.logger.info(f"Updated usage for token {token_id} in Table Storage")
                        return
                else:
                    # Create new entity
                    new_entity = {
                        "PartitionKey": token_id,
                        "RowKey": token_id,
                        "token_id": token_id,
                        "request_count": 1,
                        "last_used": now,
                        "endpoints": json.dumps({endpoint: 1}),
                        "status_codes": json.dumps({str(status_code): 1}),
                        "errors": json.dumps([
                            {
                                "timestamp": now,
                                "endpoint": endpoint,
                                "error": error
                            }
                        ] if error else [])
                    }
                    
                    success = self.table_storage.create_entity(API_KEY_USAGE_TABLE, new_entity)
                    if success:
                        self.logger.info(f"Created usage for token {token_id} in Table Storage")
                        return
            except Exception as e:
                self.logger.error(f"Failed to update usage in Table Storage: {str(e)}")
                # Fall back to SQLite
        
        # Always update SQLite as fallback
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Get current usage
        c.execute("SELECT * FROM APIKeyUsage WHERE token_id = ?", (token_id,))
        usage = c.fetchone()
        
        if not usage:
            # Initialize usage if not exists
            c.execute(
                "INSERT INTO APIKeyUsage (token_id, request_count, last_used, endpoints, status_codes, errors) VALUES (?, ?, ?, ?, ?, ?)",
                [token_id, 1, now, "{}", "{}", "[]"]
            )
            usage_data = {
                "id": token_id,
                "token_id": token_id,
                "request_count": 1,
                "last_used": now,
                "endpoints": "{}",
                "status_codes": "{}",
                "errors": "[]"
            }
        else:
            # Get current usage data
            columns = ["token_id", "request_count", "last_used", "endpoints", "status_codes", "errors"]
            usage_data = dict(zip(columns, usage))
            
            # Update usage data
            usage_data["request_count"] += 1
            usage_data["last_used"] = now
            
            # Update endpoints
            endpoints = json.loads(usage_data["endpoints"])
            endpoints[endpoint] = endpoints.get(endpoint, 0) + 1
            usage_data["endpoints"] = json.dumps(endpoints)
            
            # Update status codes
            status_codes = json.loads(usage_data["status_codes"])
            status_codes[str(status_code)] = status_codes.get(str(status_code), 0) + 1
            usage_data["status_codes"] = json.dumps(status_codes)
            
            # Update errors if any
            if error:
                errors = json.loads(usage_data["errors"])
                errors.append({
                    "timestamp": now,
                    "endpoint": endpoint,
                    "error": error
                })
                usage_data["errors"] = json.dumps(errors)
            
            # Update SQLite
            c.execute(
                """UPDATE APIKeyUsage 
                SET request_count = ?, last_used = ?, endpoints = ?, status_codes = ?, errors = ? 
                WHERE token_id = ?""",
                [
                    usage_data["request_count"],
                    usage_data["last_used"],
                    usage_data["endpoints"],
                    usage_data["status_codes"],
                    usage_data["errors"],
                    token_id
                ]
            )
        
        conn.commit()
        
        # Try to update Cosmos DB if not in fallback mode
        if not self._fallback_mode and self.cosmos_usage_container:
            try:
                # Add id field for Cosmos DB
                usage_data["id"] = token_id
                
                # Try to read existing item first
                try:
                    existing = self.cosmos_usage_container.read_item(
                        item=token_id,
                        partition_key=token_id
                    )
                    # Update existing item
                    existing.update(usage_data)
                    self.cosmos_usage_container.replace_item(
                        item=token_id,
                        body=existing,
                        partition_key=token_id
                    )
                except cosmos_exceptions.CosmosResourceNotFoundError:
                    # Create new item if not exists
                    self.cosmos_usage_container.create_item(
                        body=usage_data,
                        partition_key=token_id
                    )
                
                # Mark as synced in SQLite
                c.execute("UPDATE APIKeyUsage SET synced_to_cosmos = 1 WHERE token_id = ?", (token_id,))
                conn.commit()
            except Exception as e:
                self.logger.error(f"Failed to update usage in Cosmos DB: {str(e)}")
                # Continue with SQLite only
                self._fallback_mode = True
        
        conn.close()
        
        self.logger.info(f"Logged usage for token {token_id}: {endpoint} - {status_code}")

    def _get_db_path(self) -> str:
        """Get the database path, creating directories if needed."""
        # Make sure the directory exists
        Path(os.path.dirname(self.db_path)).mkdir(parents=True, exist_ok=True)
        return self.db_path
    
    def _get_db_connection(self) -> sqlite3.Connection:
        """Get a database connection."""
        return sqlite3.connect(self.db_path)

    async def validate_token(self, 
                   token_hash: str, 
                   client_ip: Optional[str] = None) -> Dict[str, Any]:
        """Validate a token by its hash and return token data if valid.
        
        Args:
            token_hash: The hash of the token to validate
            client_ip: Optional client IP address for restriction checking
            
        Returns:
            Dictionary with validation results
        """
        await self.init()
        
        # Try table storage first if enabled
        if self.use_table_storage and self.table_storage:
            try:
                # We can't query directly by token_hash in Table Storage efficiently
                # because it's not a PartitionKey or RowKey
                # So we need to filter post-query
                query_filter = f"token_hash eq '{token_hash}' and is_revoked eq false"
                token_entities = self.table_storage.query_entities(API_KEYS_TABLE, query_filter)
                
                if token_entities:
                    token_data = token_entities[0]
                    
                    # Check expiration
                    if token_data.get("expires_at"):
                        expires_at = datetime.fromisoformat(token_data["expires_at"].replace("Z", "+00:00"))
                        if expires_at < datetime.utcnow():
                            self.logger.warning(f"Expired token: {token_data.get('id')}")
                            return {"valid": False, "reason": "Token expired"}
                    
                    # Check IP restrictions if any
                    if token_data.get("ip_restrictions") and client_ip:
                        allowed_ips = token_data["ip_restrictions"].split(",") if token_data["ip_restrictions"] else []
                        if allowed_ips and not any(self._ip_matches(client_ip, allowed_ip) for allowed_ip in allowed_ips):
                            self.logger.warning(f"IP {client_ip} not allowed for token {token_data.get('id')}")
                            return {"valid": False, "reason": "IP address not allowed"}
                    
                    # Remove Table Storage specific fields
                    token_data.pop('PartitionKey', None)
                    token_data.pop('RowKey', None)
                    token_data.pop('odata.etag', None)
                    token_data.pop('Timestamp', None)
                    
                    # Format the response
                    return {
                        "valid": True,
                        "provider_id": token_data["provider_id"],
                        "scopes": token_data["scopes"].split(",") if token_data.get("scopes") else [],
                        "environment": token_data.get("environment", ""),
                        "token_id": token_data["id"],
                        "token_data": token_data
                    }
            except Exception as e:
                self.logger.error(f"Failed to validate token in Table Storage: {str(e)}")
                # Fall back to SQLite
        
        # Fall back to SQLite
        conn = self._get_db_connection()
        try:
            c = conn.cursor()
            
            c.execute("""
                SELECT * FROM APIKeys 
                WHERE token_hash = ? 
                AND is_revoked = 0 
                AND (expires_at IS NULL OR datetime(expires_at) > datetime('now'))
            """, (token_hash,))
            
            token = c.fetchone()
            
            if not token:
                self.logger.warning(f"Invalid or expired token hash: {token_hash}")
                return {"valid": False, "reason": "Invalid or expired token"}
            
            # Convert row to dict
            columns = [desc[0] for desc in c.description]
            token_data = dict(zip(columns, token))
            
            # Check IP restrictions if any
            if token_data["ip_restrictions"] and client_ip:
                allowed_ips = token_data["ip_restrictions"].split(",") if token_data["ip_restrictions"] else []
                if allowed_ips and not any(self._ip_matches(client_ip, allowed_ip) for allowed_ip in allowed_ips):
                    self.logger.warning(f"IP {client_ip} not allowed for token {token_data['id']}")
                    return {"valid": False, "reason": "IP address not allowed"}
            
            # Format the response
            return {
                "valid": True,
                "provider_id": token_data["provider_id"],
                "scopes": token_data["scopes"].split(",") if token_data.get("scopes") else [],
                "environment": token_data.get("environment", ""),
                "token_id": token_data["id"],
                "token_data": token_data
            }
        except Exception as e:
            self.logger.error(f"Error validating token: {str(e)}")
            return {"valid": False, "reason": f"Error validating token: {str(e)}"}
        finally:
            conn.close()
            
    def _ip_matches(self, client_ip: str, allowed_ip: str) -> bool:
        """Check if client IP matches allowed IP or CIDR.
        
        Args:
            client_ip: Client IP address
            allowed_ip: Allowed IP or CIDR range
            
        Returns:
            True if client IP is allowed, False otherwise
        """
        if not allowed_ip or not client_ip:
            return False
            
        try:
            from ipaddress import ip_address, ip_network
            
            # Check if it's a CIDR range
            if '/' in allowed_ip:
                network = ip_network(allowed_ip)
                client = ip_address(client_ip)
                return client in network
            
            # Simple IP matching
            return ip_address(client_ip) == ip_address(allowed_ip)
        except Exception as e:
            self.logger.error(f"Error in IP matching: {str(e)}")
            return False

    async def is_token_revoked(self, token_id: str) -> bool:
        """Check if a token is revoked.
        
        Args:
            token_id: The ID of the token to check
            
        Returns:
            True if the token is revoked, False otherwise
        """
        await self.init()
        
        # Try table storage first if enabled
        if self.use_table_storage and self.table_storage:
            try:
                # Query for the token with the given ID
                # Need to search across all partition keys since we don't know the provider_id
                query_filter = f"RowKey eq '{token_id}'"
                token_entities = self.table_storage.query_entities(API_KEYS_TABLE, query_filter)
                
                if token_entities:
                    token_data = token_entities[0]
                    # Check if token is revoked
                    return token_data.get("is_revoked", False) is True
                
                # Token not found, consider it revoked for security
                self.logger.warning(f"Token {token_id} not found in Table Storage, considering revoked")
                return True
            except Exception as e:
                self.logger.error(f"Failed to check token revocation in Table Storage: {str(e)}")
                # Fall back to SQLite
        
        # Try Cosmos DB if not in fallback mode
        if not self._fallback_mode and self.cosmos_container:
            try:
                # We need to query by ID since we don't know the partition key (provider_id)
                query = f"SELECT * FROM c WHERE c.id = @token_id"
                params = [{"name": "@token_id", "value": token_id}]
                items = list(self.cosmos_container.query_items(
                    query=query,
                    parameters=params,
                    enable_cross_partition_query=True
                ))
                
                if items:
                    return items[0].get("is_revoked", False) is True
                
                # Token not found, consider it revoked for security
                self.logger.warning(f"Token {token_id} not found in Cosmos DB, considering revoked")
                return True
            except Exception as e:
                self.logger.error(f"Failed to check token revocation in Cosmos DB: {str(e)}")
                self._fallback_mode = True
        
        # Fall back to SQLite
        conn = self._get_db_connection()
        try:
            c = conn.cursor()
            c.execute("SELECT is_revoked FROM APIKeys WHERE id = ?", (token_id,))
            result = c.fetchone()
            
            if result is None:
                # Token not found, consider it revoked for security
                self.logger.warning(f"Token {token_id} not found in SQLite, considering revoked")
                return True
                
            return result[0] == 1  # SQLite stores booleans as 0/1
        except Exception as e:
            self.logger.error(f"Error checking token revocation: {str(e)}")
            # In case of error, consider the token revoked for security
            return True
        finally:
            conn.close() 

    async def test_table_storage(self) -> Dict[str, Any]:
        """Test method to verify if the table storage module is working correctly.
        
        Returns:
            Dictionary with test results
        """
        await self.init()
        
        results = {
            "table_storage_enabled": self.use_table_storage,
            "table_storage_initialized": False,
            "tables_available": [],
            "connection_string_available": bool(self.table_connection_string),
            "test_operations": {}
        }
        
        if not self.use_table_storage or not self.table_storage:
            return results
            
        # Check if table storage is initialized
        results["table_storage_initialized"] = self.table_storage._initialized
        
        # Check available tables
        if self.table_storage.tables:
            results["tables_available"] = list(self.table_storage.tables.keys())
            
        # Try basic operations if tables exist
        if API_KEYS_TABLE in self.table_storage.tables:
            # Test query
            try:
                test_query = self.table_storage.query_entities(API_KEYS_TABLE, "RowKey ne ''", "id,provider_id")
                results["test_operations"]["query"] = {
                    "success": True,
                    "count": len(test_query)
                }
            except Exception as e:
                results["test_operations"]["query"] = {
                    "success": False,
                    "error": str(e)
                }
        
        return results 