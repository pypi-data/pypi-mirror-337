"""
API Key Router - Dedicated endpoints for API key management.
"""

from fastapi import APIRouter, HTTPException, Depends, Request, BackgroundTasks, Security
from fastapi.security.api_key import APIKeyHeader
from typing import List, Dict, Any
import os
import asyncio
from datetime import datetime
import azure.cosmos.cosmos_client as cosmos_client_module
import base64
import hashlib

from api_keys.models import (
    KeyRequest, KeyResponse, RevokeRequest, TokenUsage, 
    BatchUsageUpdate, BatchOperationsRequest, BatchOperation
)
from api_keys.services.api_key_service import APIKeyService
from api_keys.services.db_transaction import TransactionManager

# Define API key header
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# Create router
router = APIRouter(prefix="/keys", tags=["API Keys"])

# Initialize transaction manager
transaction_manager = None

def get_transaction_manager():
    """Get or initialize transaction manager."""
    global transaction_manager
    if transaction_manager is None:
        db_path = os.getenv("DB_PATH", "/data/api_keys.db")
        cosmos_connection = os.getenv("AZURE_COSMODB_CONNECTION_STRING")
        
        if cosmos_connection:
            cosmos_db = cosmos_client_module.CosmosClient.from_connection_string(
                cosmos_connection,
                retry_total=3,
                retry_backoff_max=15
            )
        else:
            cosmos_db = None
        
        transaction_manager = TransactionManager(db_path, cosmos_db)
    
    return transaction_manager

# Dependency to get API key service
async def get_api_key_service():
    """Get API key service."""
    service = APIKeyService()
    await service.init()
    return service

# Dependency for API key validation
async def get_api_key(
    request: Request,
    api_key: str = Security(api_key_header),
    api_key_service: APIKeyService = Depends(get_api_key_service)
):
    """Validate API key."""
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API key is required"
        )
    
    # Get client IP
    client_ip = request.client.host if request.client else None
    
    # Validate API key with IP check
    key_data = await api_key_service.validate_api_key(api_key, client_ip)
    
    if not key_data.get("valid"):
        raise HTTPException(
            status_code=401,
            detail=key_data.get("reason", "Invalid API key")
        )
    
    return key_data

async def log_request(request: Request, token_id: str, api_key_service: APIKeyService):
    """Log the API request."""
    try:
        await api_key_service.token_service.log_token_usage(
            token_id=token_id,
            endpoint=str(request.url.path),
            status_code=200
        )
    except Exception as e:
        # Log error but don't fail the request
        api_key_service.logger.error(f"Failed to log usage: {str(e)}")

@router.post("/batch/usage", status_code=202)
async def batch_update_usage(
    updates: BatchUsageUpdate,
    background_tasks: BackgroundTasks,
    transaction_mgr: TransactionManager = Depends(get_transaction_manager)
):
    """
    Batch update usage statistics for multiple tokens.
    This endpoint is optimized for high-volume updates.
    """
    try:
        # Add updates to batch processing queue
        for update in updates.updates:
            background_tasks.add_task(transaction_mgr.batch_update, update.dict())
        
        return {
            "status": "accepted",
            "message": f"Processing {len(updates.updates)} updates",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to queue batch updates: {str(e)}"
        )

@router.post("/generate", response_model=KeyResponse)
async def generate_key(
    request: KeyRequest,
    api_key_service: APIKeyService = Depends(get_api_key_service)
):
    """Generate a new API key."""
    try:
        # Create API key
        token_data, raw_token = await api_key_service.create_api_key(
            provider_id=request.provider_id,
            name=request.name,
            environment=request.environment,
            scopes=request.scopes,
            expires_in_days=request.expires_in_days,
            description=request.description,
            ip_restrictions=request.ip_restrictions
        )
        
        # Return response
        return KeyResponse(
            key=raw_token,
            token_info=token_data
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate API key: {str(e)}")

def mask_sensitive_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mask sensitive fields in the response data.
    Uses a combination of hashing and encoding for sensitive fields.
    """
    if not isinstance(data, dict):
        return data
        
    masked = data.copy()
    sensitive_fields = ['provider_id', 'metadata', 'ip_restrictions']
    
    for field in sensitive_fields:
        if field in masked:
            # Create a deterministic but masked version of sensitive fields
            if masked[field]:
                value = str(masked[field])
                # Create a keyed hash using the original value
                h = hashlib.blake2b(key=b'api_key_service', digest_size=16)
                h.update(value.encode())
                # Use base64 for a URL-safe representation
                masked[field] = base64.urlsafe_b64encode(h.digest()).decode()
    
    return masked

@router.get("", response_model=List[Dict[str, Any]])
async def list_keys(
    provider_id: str,
    key_data = Depends(get_api_key),
    api_key_service: APIKeyService = Depends(get_api_key_service)
):
    """List all API keys for a provider."""
    # Verify the API key belongs to the requested provider
    if key_data["provider_id"] != provider_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access keys for this provider"
        )
    
    try:
        keys = await api_key_service.list_api_keys(provider_id)
        # Mask sensitive data in response
        return [mask_sensitive_data(key) for key in keys]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list API keys: {str(e)}")

@router.post("/{token_id}/revoke")
async def revoke_key(
    token_id: str,
    request: RevokeRequest,
    key_data = Depends(get_api_key),
    api_key_service: APIKeyService = Depends(get_api_key_service)
):
    """Revoke an API key."""
    try:
        # Get the token to verify ownership
        tokens = await api_key_service.list_api_keys(key_data["provider_id"])
        token = next((t for t in tokens if t["id"] == token_id), None)
        
        if not token:
            raise HTTPException(
                status_code=404,
                detail="API key not found"
            )
            
        if token["provider_id"] != key_data["provider_id"]:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to revoke this API key"
            )
        
        return await api_key_service.revoke_api_key(token_id, request.reason)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to revoke API key: {str(e)}")

@router.get("/{token_id}/usage")
async def get_key_usage(
    token_id: str,
    key_data = Depends(get_api_key),
    api_key_service: APIKeyService = Depends(get_api_key_service)
):
    """Get usage statistics for an API key."""
    try:
        # Get the token to verify ownership
        tokens = await api_key_service.list_api_keys(key_data["provider_id"])
        token = next((t for t in tokens if t["id"] == token_id), None)
        
        if not token:
            raise HTTPException(
                status_code=404,
                detail="API key not found"
            )
            
        if token["provider_id"] != key_data["provider_id"]:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to access usage for this API key"
            )
        
        usage_data = await api_key_service.get_api_key_usage(token_id)
        return mask_sensitive_data(usage_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get API key usage: {str(e)}")

@router.post("/batch/operations")
async def batch_operations(
    request: BatchOperationsRequest,
    api_key_service: APIKeyService = Depends(get_api_key_service)
):
    """
    Execute multiple API key operations in parallel.
    This endpoint allows executing different types of operations concurrently:
    - get_usage: Get usage statistics for an API key
    - revoke: Revoke an API key
    - list: List all API keys for a provider
    
    Each operation is executed independently and in parallel.
    If one operation fails, it won't affect the others.
    """
    async def execute_operation(op: BatchOperation) -> Dict[str, Any]:
        try:
            if op.operation == "get_usage":
                return await api_key_service.get_api_key_usage(op.params["token_id"])
            elif op.operation == "revoke":
                return await api_key_service.revoke_api_key(
                    op.params["token_id"], 
                    op.params["reason"]
                )
            elif op.operation == "list":
                return await api_key_service.list_api_keys(op.params["provider_id"])
            else:
                return {"error": f"Unknown operation: {op.operation}"}
        except Exception as e:
            return {
                "error": str(e),
                "operation": op.operation,
                "params": op.params
            }
    
    # Execute operations in parallel
    tasks = [execute_operation(op) for op in request.operations]
    results = await asyncio.gather(*tasks)
    
    return {
        "results": results,
        "total": len(results),
        "successful": len([r for r in results if "error" not in r]),
        "failed": len([r for r in results if "error" in r]),
        "timestamp": datetime.utcnow().isoformat()
    } 