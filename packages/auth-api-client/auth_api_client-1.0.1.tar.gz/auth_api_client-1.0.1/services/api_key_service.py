"""
API Key Service - Dedicated service for API key management.
This service encapsulates the logic for creating, validating, and managing API keys.
"""

from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import logging
from fastapi import HTTPException
import hashlib
from ipaddress import ip_address, IPv4Address, IPv6Address

from .token_service import TokenService

logger = logging.getLogger(__name__)

# Singleton instance
_instance = None

class APIKeyService:
    """Service for API key management"""
    
    def __new__(cls, token_service: TokenService = None):
        """Ensure singleton instance."""
        global _instance
        if _instance is None:
            _instance = super(APIKeyService, cls).__new__(cls)
            _instance.token_service = token_service or TokenService()
            _instance.logger = logging.getLogger(__name__)
            _instance._initialized = False
        return _instance
    
    def __init__(self, token_service: TokenService = None):
        """Initialize API key service."""
        # No-op since initialization is done in __new__
        pass
        
    async def init(self):
        """Initialize the service."""
        if not self._initialized:
            await self.token_service.init()
            self._initialized = True
        
    async def create_api_key(
        self, 
        provider_id: str, 
        name: str, 
        environment: str,
        scopes: List[str] = ["api:access"],
        expires_in_days: Optional[int] = 365,
        description: Optional[str] = None,
        ip_restrictions: Optional[List[str]] = None
    ) -> Tuple[Dict[str, Any], str]:
        """Create a new API key."""
        try:
            # Validate environment
            if environment not in ["test", "live"]:
                raise ValueError("Environment must be 'test' or 'live'")
                
            # Create token
            token_data, raw_token = await self.token_service.create_token(
                provider_id=provider_id,
                name=name,
                scopes=scopes,
                environment=environment,
                expires_in_days=expires_in_days,
                description=description,
                ip_restrictions=ip_restrictions
            )
            
            return token_data, raw_token
        except Exception as e:
            self.logger.error(f"Error creating API key: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to create API key: {str(e)}")
    
    async def list_api_keys(self, provider_id: str) -> List[Dict[str, Any]]:
        """List all API keys for a provider."""
        try:
            return await self.token_service.list_tokens(provider_id)
        except Exception as e:
            self.logger.error(f"Error listing API keys: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to list API keys: {str(e)}")
    
    async def revoke_api_key(self, token_id: str, reason: str) -> Dict[str, Any]:
        """Revoke an API key."""
        try:
            return await self.token_service.revoke_token(token_id, reason)
        except ValueError as e:
            self.logger.error(f"Error revoking API key: {str(e)}")
            raise HTTPException(status_code=404, detail=f"API key not found: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error revoking API key: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to revoke API key: {str(e)}")
    
    async def get_api_key_usage(self, token_id: str) -> Dict[str, Any]:
        """Get usage statistics for an API key."""
        try:
            return await self.token_service.get_api_key_usage(token_id)
        except ValueError as e:
            self.logger.error(f"Error getting API key usage: {str(e)}")
            raise HTTPException(status_code=404, detail=f"API key usage not found: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error getting API key usage: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to get API key usage: {str(e)}")
    
    async def validate_api_key(self, api_key: str, client_ip: Optional[str] = None) -> Dict[str, Any]:
        """Validate an API key and return its data if valid."""
        try:
            # Ensure service is initialized
            await self.init()
            
            # Hash the API key for comparison
            token_hash = hashlib.sha256(api_key.encode()).hexdigest()
            
            # Use the token service's validate_token method
            validation_result = await self.token_service.validate_token(token_hash, client_ip)
            
            if validation_result.get("valid", False):
                # Format the response for API compatibility
                return {
                    "valid": True,
                    "provider_id": validation_result["provider_id"],
                    "scopes": validation_result["scopes"],
                    "environment": validation_result["environment"],
                    "token_id": validation_result["token_id"]
                }
            else:
                return validation_result
                
        except Exception as e:
            self.logger.error(f"Error validating API key: {str(e)}")
            return {"valid": False, "reason": "Error validating API key"}
    
    def _ip_matches(self, client_ip: str, allowed_ip: str) -> bool:
        """Check if client IP matches allowed IP or CIDR."""
        try:
            if '/' in allowed_ip:  # CIDR notation
                network = ip_network(allowed_ip)
                return ip_address(client_ip) in network
            else:
                return ip_address(client_ip) == ip_address(allowed_ip)
        except ValueError:
            return False 