"""
Database Transaction Manager - Handles database transactions with proper locking mechanisms.
"""

import asyncio
import contextlib
import sqlite3
import os
import json
from typing import Optional, Any, Dict
import logging
from datetime import datetime
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as cosmos_exceptions
from azure.cosmos.partition_key import PartitionKey

logger = logging.getLogger(__name__)

class DatabaseLock:
    """Distributed locking mechanism for database operations."""
    
    def __init__(self):
        self._locks = {}
        self._lock = asyncio.Lock()
    
    async def acquire(self, key: str, timeout: float = 5.0) -> bool:
        """Acquire a lock for a specific key."""
        try:
            async with asyncio.timeout(timeout):
                if key not in self._locks:
                    async with self._lock:
                        if key not in self._locks:
                            self._locks[key] = asyncio.Lock()
                
                await self._locks[key].acquire()
                return True
        except asyncio.TimeoutError:
            logger.warning(f"Timeout acquiring lock for key: {key}")
            return False
    
    def release(self, key: str) -> None:
        """Release a lock for a specific key."""
        if key in self._locks and self._locks[key].locked():
            self._locks[key].release()

class TransactionManager:
    """Manages database transactions with proper locking."""
    
    def __init__(self, sqlite_path: str, cosmos_client: Optional[cosmos_client.CosmosClient] = None):
        self.sqlite_path = sqlite_path
        self.cosmos_client = cosmos_client
        self.lock_manager = DatabaseLock()
        self._batch_queue = asyncio.Queue()
        self._processing = False
    
    @contextlib.asynccontextmanager
    async def transaction(self, key: str):
        """Context manager for database transactions."""
        acquired = await self.lock_manager.acquire(key)
        if not acquired:
            raise TimeoutError(f"Could not acquire lock for key: {key}")
        
        conn = sqlite3.connect(self.sqlite_path)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            self.lock_manager.release(key)
    
    async def batch_update(self, updates: Dict[str, Any]) -> None:
        """Add updates to the batch queue."""
        await self._batch_queue.put(updates)
        
        if not self._processing:
            self._processing = True
            asyncio.create_task(self._process_batch())
    
    async def _process_batch(self) -> None:
        """Process batched updates."""
        try:
            batch = []
            batch_size = int(os.getenv("COSMOS_BATCH_SIZE", "100"))
            batch_interval = int(os.getenv("BATCH_PROCESSING_INTERVAL", "5"))
            
            while True:
                try:
                    # Collect updates for the batch interval
                    async with asyncio.timeout(batch_interval):
                        while len(batch) < batch_size:
                            update = await self._batch_queue.get()
                            batch.append(update)
                            self._batch_queue.task_done()
                except asyncio.TimeoutError:
                    if not batch:
                        # No updates to process
                        break
                
                # Process the batch
                if batch:
                    await self._execute_batch(batch)
                    batch = []
        
        except Exception as e:
            logger.error(f"Error processing batch: {str(e)}")
        finally:
            self._processing = False
            
            # If there are still items in the queue, start a new processing task
            if not self._batch_queue.empty():
                self._processing = True
                asyncio.create_task(self._process_batch())
    
    async def _execute_batch(self, batch: list) -> None:
        """Execute a batch of updates."""
        # Group updates by token_id
        updates_by_token = {}
        for update in batch:
            token_id = update["token_id"]
            if token_id not in updates_by_token:
                updates_by_token[token_id] = []
            updates_by_token[token_id].append(update)
        
        # Process each token's updates
        for token_id, token_updates in updates_by_token.items():
            try:
                async with self.transaction(token_id):
                    # Combine updates for the same token
                    combined_update = self._combine_updates(token_updates)
                    
                    # Update SQLite
                    await self._update_sqlite(token_id, combined_update)
                    
                    # Update Cosmos DB if available
                    if self.cosmos_client:
                        await self._update_cosmos(token_id, combined_update)
            except Exception as e:
                logger.error(f"Error processing updates for token {token_id}: {str(e)}")
    
    def _combine_updates(self, updates: list) -> Dict[str, Any]:
        """Combine multiple updates for the same token."""
        if not updates:
            return {}
        
        combined = {
            "token_id": updates[0]["token_id"],
            "request_count": 0,
            "last_used": None,
            "endpoints": {},
            "status_codes": {},
            "errors": []
        }
        
        for update in updates:
            combined["request_count"] += update.get("request_count", 0)
            
            if update.get("last_used"):
                if not combined["last_used"] or update["last_used"] > combined["last_used"]:
                    combined["last_used"] = update["last_used"]
            
            # Merge endpoints
            for endpoint, count in update.get("endpoints", {}).items():
                combined["endpoints"][endpoint] = combined["endpoints"].get(endpoint, 0) + count
            
            # Merge status codes
            for code, count in update.get("status_codes", {}).items():
                combined["status_codes"][code] = combined["status_codes"].get(code, 0) + count
            
            # Append errors
            combined["errors"].extend(update.get("errors", []))
        
        return combined
    
    async def _update_sqlite(self, token_id: str, update: Dict[str, Any]) -> None:
        """Update SQLite with combined updates."""
        conn = sqlite3.connect(self.sqlite_path)
        try:
            c = conn.cursor()
            
            # Update or insert usage data
            c.execute("""
                INSERT INTO APIKeyUsage (
                    token_id, request_count, last_used, endpoints, status_codes, errors
                ) VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(token_id) DO UPDATE SET
                    request_count = request_count + ?,
                    last_used = ?,
                    endpoints = ?,
                    status_codes = ?,
                    errors = ?,
                    synced_to_cosmos = 0
            """, [
                token_id,
                update["request_count"],
                update["last_used"],
                json.dumps(update["endpoints"]),
                json.dumps(update["status_codes"]),
                json.dumps(update["errors"]),
                update["request_count"],
                update["last_used"],
                json.dumps(update["endpoints"]),
                json.dumps(update["status_codes"]),
                json.dumps(update["errors"])
            ])
            
            conn.commit()
        finally:
            conn.close()
    
    async def _update_cosmos(self, token_id: str, update: Dict[str, Any]) -> None:
        """Update Cosmos DB with combined updates."""
        try:
            container = self.cosmos_client.get_database_client(os.getenv("AZURE_COSMODB_DATABASE", "api_keys")) \
                           .get_container_client("APIKeyUsage")
            
            # Try to read existing document
            try:
                doc = container.read_item(item=token_id, partition_key=token_id)
                
                # Update existing document
                doc["request_count"] += update["request_count"]
                doc["last_used"] = update["last_used"]
                
                # Merge endpoints
                for endpoint, count in update["endpoints"].items():
                    doc["endpoints"][endpoint] = doc["endpoints"].get(endpoint, 0) + count
                
                # Merge status codes
                for code, count in update["status_codes"].items():
                    doc["status_codes"][code] = doc["status_codes"].get(code, 0) + count
                
                # Append errors
                doc["errors"].extend(update["errors"])
                
                # Update document
                container.replace_item(item=token_id, body=doc)
            
            except cosmos_exceptions.CosmosResourceNotFoundError:
                # Create new document
                update["id"] = token_id
                container.create_item(body=update)
        
        except Exception as e:
            logger.error(f"Error updating Cosmos DB: {str(e)}")
            # Mark for retry in background sync 