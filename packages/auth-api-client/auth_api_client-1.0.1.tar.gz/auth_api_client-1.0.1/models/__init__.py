"""
API Key Management Models
"""

from typing import List, Optional, Dict, Any, Literal
from datetime import datetime
from pydantic import BaseModel, Field

class KeyRequest(BaseModel):
    """Model for API key generation request."""
    provider_id: str
    name: str
    environment: str = "test"
    scopes: List[str] = ["api:access"]
    expires_in_days: Optional[int] = 365
    description: Optional[str] = None
    ip_restrictions: Optional[List[str]] = None

class KeyResponse(BaseModel):
    """Model for API key generation response."""
    key: str
    token_info: Dict[str, Any]

class RevokeRequest(BaseModel):
    """Model for token revocation request."""
    reason: str

class TokenUsage(BaseModel):
    """Model for token usage statistics."""
    token_id: str
    request_count: int
    last_used: Optional[datetime] = None
    endpoints: Dict[str, int] = {}
    status_codes: Dict[str, int] = {}
    errors: List[Dict[str, Any]] = []

class UsageUpdate(BaseModel):
    """Model for individual usage update."""
    token_id: str
    request_count: int = 1
    last_used: Optional[str] = None
    endpoints: Dict[str, int] = {}
    status_codes: Dict[str, int] = {}
    errors: List[Dict[str, Any]] = []

class BatchUsageUpdate(BaseModel):
    """Model for batch usage updates."""
    updates: List[UsageUpdate]
    
    class Config:
        schema_extra = {
            "example": {
                "updates": [
                    {
                        "token_id": "token-123",
                        "request_count": 1,
                        "last_used": "2025-03-25T19:07:14.094627",
                        "endpoints": {"/api/v1/data": 1},
                        "status_codes": {"200": 1},
                        "errors": []
                    },
                    {
                        "token_id": "token-456",
                        "request_count": 2,
                        "last_used": "2025-03-25T19:07:15.094627",
                        "endpoints": {"/api/v1/users": 2},
                        "status_codes": {"200": 1, "404": 1},
                        "errors": [
                            {
                                "timestamp": "2025-03-25T19:07:15.094627",
                                "endpoint": "/api/v1/users",
                                "error": "Resource not found"
                            }
                        ]
                    }
                ]
            }
        }

class BatchOperation(BaseModel):
    """Model for a single batch operation."""
    operation: Literal["get_usage", "revoke", "list"]
    params: Dict[str, Any]

class BatchOperationsRequest(BaseModel):
    """Model for batch operations request."""
    operations: List[BatchOperation]
    
    class Config:
        schema_extra = {
            "example": {
                "operations": [
                    {
                        "operation": "get_usage",
                        "params": {
                            "token_id": "token-123"
                        }
                    },
                    {
                        "operation": "revoke",
                        "params": {
                            "token_id": "token-456",
                            "reason": "Security policy update"
                        }
                    },
                    {
                        "operation": "list",
                        "params": {
                            "provider_id": "provider-789"
                        }
                    }
                ]
            }
        } 