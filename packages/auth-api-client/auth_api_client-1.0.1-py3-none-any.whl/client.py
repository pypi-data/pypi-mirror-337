"""
Auth API Client Library

A robust client for interacting with the Auth API service with built-in
retry logic, validation, and error handling.
"""

import json
import time
import uuid
import logging
import requests
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime, timezone, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("auth_api_client")

class AuthAPIError(Exception):
    """Base exception for API client errors"""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Any] = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)

class ValidationError(AuthAPIError):
    """Data validation error"""
    pass

class AuthenticationError(AuthAPIError):
    """Authentication or authorization error"""
    pass

class RateLimitError(AuthAPIError):
    """Rate limit exceeded error"""
    pass

class ServerError(AuthAPIError):
    """Server-side error"""
    pass

class ClientError(AuthAPIError):
    """Client-side error"""
    pass

class TimeoutError(AuthAPIError):
    """Request timeout error"""
    pass

class KeyGenerationError(AuthAPIError):
    """Error specifically for key generation issues"""
    pass

class AuthAPIClient:
    """
    Client for the Auth API service with retry logic, validation, and error handling.
    
    Features:
    - Automatic retries with exponential backoff
    - Request validation
    - Consistent error handling
    - Detailed logging
    """
    
    def __init__(
        self, 
        base_url: str = "http://localhost:8000",
        api_key: Optional[str] = None,
        key_id: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        timeout: float = 10.0,
        verify_ssl: bool = True,
        log_level: int = logging.INFO
    ):
        """
        Initialize the Auth API client.
        
        Args:
            base_url: Base URL of the Auth API service
            api_key: API key for authentication
            key_id: Optional ID of the API key for tracking
            max_retries: Maximum number of retry attempts for failed requests
            retry_delay: Base delay between retries in seconds
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
            log_level: Logging level
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.key_id = key_id
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        # Configure logger
        self.logger = logger
        self.logger.setLevel(log_level)
        
        # If API key is provided but key_id is not, try to fetch it
        if self.api_key and not self.key_id:
            try:
                self._fetch_key_id()
            except Exception as e:
                self.logger.warning(f"Could not fetch key ID automatically: {str(e)}")
    
    def _get_headers(self, additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Get request headers including authentication if available"""
        headers = {"Content-Type": "application/json"}
        
        if self.api_key:
            headers["X-API-Key"] = self.api_key
            
        if additional_headers:
            headers.update(additional_headers)
            
        return headers
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle API response and raise appropriate exceptions for errors
        
        Args:
            response: Response object from requests
            
        Returns:
            Response data as dictionary
            
        Raises:
            AuthenticationError: For 401/403 errors
            ValidationError: For 422 errors
            RateLimitError: For 429 errors
            ClientError: For other 4xx errors
            ServerError: For 5xx errors
        """
        status_code = response.status_code
        
        # Handle successful responses
        if 200 <= status_code < 300:
            try:
                return response.json()
            except ValueError:
                return {"content": response.text}
        
        # Handle error responses
        error_message = f"API request failed with status {status_code}"
        error_details = None
        
        try:
            error_data = response.json()
            if isinstance(error_data, dict):
                if "detail" in error_data:
                    error_message = error_data["detail"]
                error_details = error_data
        except (ValueError, KeyError):
            if response.text:
                error_message = response.text
        
        # Map status codes to error types
        if status_code == 401 or status_code == 403:
            raise AuthenticationError(error_message, status_code, response)
        elif status_code == 422:
            raise ValidationError(error_message, status_code, response)
        elif status_code == 429:
            raise RateLimitError(error_message, status_code, response)
        elif 400 <= status_code < 500:
            raise ClientError(error_message, status_code, response)
        elif 500 <= status_code < 600:
            # Enhanced error for server errors
            server_error = f"{error_message}. Server Error Details: {error_details if error_details else 'Not available'}"
            raise ServerError(server_error, status_code, response)
        else:
            raise AuthAPIError(error_message, status_code, response)
    
    def _request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        retry_on_statuses: Tuple[int, ...] = (429, 500, 502, 503, 504),
        disable_retries: bool = False
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the API with retry logic
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            data: Request data
            params: Query parameters
            headers: Additional headers
            retry_on_statuses: Status codes that should trigger a retry
            disable_retries: Whether to disable retry logic
            
        Returns:
            Response data as dictionary
        """
        url = f"{self.base_url}{endpoint}"
        all_headers = self._get_headers(headers)
        method = method.upper()
        
        self.logger.debug(f"Making {method} request to {url}")
        if params:
            self.logger.debug(f"Query params: {params}")
        if data:
            self.logger.debug(f"Request data: {data}")
        
        # Retry loop
        last_exception = None
        for attempt in range(self.max_retries if not disable_retries else 1):
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                    headers=all_headers,
                    timeout=self.timeout,
                    verify=self.verify_ssl
                )
                
                # If status code is not in retry_on_statuses, process the response
                if response.status_code not in retry_on_statuses:
                    return self._handle_response(response)
                
                # Otherwise, prepare for retry if not the last attempt
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2 ** attempt)
                    self.logger.warning(
                        f"Request failed with status {response.status_code}. "
                        f"Retrying in {delay:.2f}s (attempt {attempt + 1}/{self.max_retries})"
                    )
                    time.sleep(delay)
                else:
                    # Last attempt failed, handle the response
                    return self._handle_response(response)
            
            except (requests.RequestException, TimeoutError) as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2 ** attempt)
                    self.logger.warning(
                        f"Request failed with error: {str(e)}. "
                        f"Retrying in {delay:.2f}s (attempt {attempt + 1}/{self.max_retries})"
                    )
                    time.sleep(delay)
                else:
                    self.logger.error(f"Request failed after {self.max_retries} attempts: {str(e)}")
                    raise TimeoutError(f"Request failed after {self.max_retries} attempts: {str(e)}")
        
        # If we get here, all retries failed with connection/timeout issues
        if last_exception:
            raise TimeoutError(f"Request failed after {self.max_retries} attempts: {str(last_exception)}")
        
        # Fallback error (shouldn't be reached)
        raise AuthAPIError("Request failed for unknown reason")
    
    def _fetch_key_id(self) -> None:
        """
        Fetch the key ID for the current API key by calling the protected endpoint
        and extracting it from the response.
        
        This is used when an API key is provided without its corresponding ID.
        """
        if not self.api_key:
            return
        
        try:
            # Call protected endpoint which should return key details
            self.logger.debug("Attempting to fetch key ID from protected endpoint")
            response = self.protected_endpoint()
            
            # Extract key ID from response
            if "key_id" in response:
                self.key_id = response["key_id"]
                self.logger.info(f"Successfully retrieved key ID: {self.key_id}")
            elif "token_id" in response:
                self.key_id = response["token_id"]
                self.logger.info(f"Successfully retrieved token ID: {self.key_id}")
            else:
                # Try to extract from introspection endpoint if available
                self.logger.debug("Key ID not found in protected endpoint, trying introspection")
                self._fetch_key_id_from_introspection()
        except Exception as e:
            self.logger.warning(f"Failed to fetch key ID: {str(e)}")
    
    def _fetch_key_id_from_introspection(self) -> None:
        """
        Alternative method to fetch key ID using an introspection endpoint
        if available in the API.
        """
        try:
            # Some APIs have dedicated endpoints for key introspection
            response = self._request("GET", "/auth/keys/introspect")
            if "id" in response:
                self.key_id = response["id"]
                self.logger.info(f"Successfully retrieved key ID from introspection: {self.key_id}")
            elif "token_id" in response:
                self.key_id = response["token_id"]
                self.logger.info(f"Successfully retrieved token ID from introspection: {self.key_id}")
        except Exception as e:
            self.logger.warning(f"Failed to fetch key ID from introspection: {str(e)}")
            
            # Try to extract from list of keys if user has permission
            self._try_fetch_key_id_from_list()
            
            # If still no key ID, try to extract from the key itself if it follows a pattern
            if not self.key_id and self.api_key:
                self._extract_key_id_from_key()

    def _try_fetch_key_id_from_list(self) -> None:
        """
        Try to find the key ID by querying the list of keys, using provider_id
        if we can extract it from a protected endpoint call.
        """
        try:
            # First try to get provider ID from protected endpoint
            provider_id = None
            try:
                result = self.protected_endpoint()
                provider_id = result.get("provider_id")
            except Exception:
                pass
                
            if not provider_id:
                self.logger.debug("Cannot list keys: no provider ID available")
                return
                
            # Now try to list keys with the provider ID
            keys = self.list_api_keys(provider_id=provider_id)
            self.logger.debug(f"Retrieved {len(keys)} keys for provider {provider_id}")
            
            # Try to find our key in the list
            for key in keys:
                # Here we'd need the actual structure of the key object
                # This is just a placeholder - adjust based on actual API response
                if "key_hash" in key and self.api_key.endswith(key["key_hash"][-8:]):
                    self.key_id = key.get("id")
                    self.logger.info(f"Found matching key ID: {self.key_id}")
                    return
        except Exception as e:
            self.logger.warning(f"Failed to fetch key ID from key list: {str(e)}")
    
    def _extract_key_id_from_key(self) -> None:
        """
        Try to extract key ID from the key itself if it follows a pattern.
        Many API systems encode information in the key string.
        """
        try:
            # If the key follows a pattern like 'permas_test_[base58_or_hex_string]'
            # where the hex string might be a representation of the UUID
            
            # Example for keys that have the format where the last part is actually the key ID
            # in an encoded form (common in some API systems)
            
            # Pattern: If key is in format "prefix_environment_encodedID"
            parts = self.api_key.split('_')
            
            if len(parts) >= 3:
                # Try to extract UUID from the key if it might be there
                import base64
                import uuid
                import re
                
                # Option 1: Try to use the last part as a direct UUID
                try:
                    # Example: If the ID part follows a pattern or is a UUID
                    if re.match(r'^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$', parts[-1]):
                        self.key_id = parts[-1]
                        self.logger.info(f"Extracted key ID from key format: {self.key_id}")
                        return
                except Exception:
                    pass
                
                # Option 2: Generate a deterministic UUID based on the API key
                # This works if the API system uses the key itself to generate the ID
                try:
                    # Create a UUID5 with the API key as namespace
                    # This is useful if the API uses a deterministic mapping from key to ID
                    namespace = uuid.UUID('00000000-0000-0000-0000-000000000000')
                    self.key_id = str(uuid.uuid5(namespace, self.api_key))
                    self.logger.info(f"Generated deterministic key ID: {self.key_id}")
                    return
                except Exception:
                    pass
                
                # Note: In a real implementation, you would need to know exactly how
                # your API keys map to IDs. This method is just a demonstration of
                # possible approaches.
                
        except Exception as e:
            self.logger.warning(f"Failed to extract key ID from key: {str(e)}")
            
        # Final fallback: Store a stub ID to allow operations that require an ID
        # This is better than failing but should be used with caution
        self.key_id = f"generated-{uuid.uuid4()}"
        self.logger.warning(
            f"Could not determine real key ID. Using generated placeholder: {self.key_id}. "
            "Usage tracking and some operations may not work correctly."
        )

    # ----------------------
    # Health/Status Endpoints
    # ----------------------
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check if the API is healthy
        
        Returns:
            Health status information
        """
        return self._request("GET", "/health")
    
    def public_endpoint(self) -> Dict[str, Any]:
        """
        Call the public endpoint
        
        Returns:
            Response from public endpoint
        """
        return self._request("GET", "/public")
    
    def protected_endpoint(self) -> Dict[str, Any]:
        """
        Call the protected endpoint (requires API key)
        
        Returns:
            Response from protected endpoint
            
        Raises:
            AuthenticationError: If not authenticated or unauthorized
        """
        if not self.api_key:
            raise ValidationError("API key is required for this endpoint")
            
        return self._request("GET", "/protected")
    
    # ----------------------
    # API Key Management
    # ----------------------
    
    def generate_api_key(
        self,
        provider_id: str,
        name: str,
        scopes: List[str],
        environment: str = "production",
        expires_in_days: int = 365,
        description: Optional[str] = None,
        ip_restrictions: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a new API key
        
        Args:
            provider_id: Provider identifier
            name: Key name
            scopes: List of permission scopes
            environment: Environment (production, staging, test)
            expires_in_days: Number of days until expiration
            description: Optional description
            ip_restrictions: Optional list of allowed IP addresses
            metadata: Optional metadata
            
        Returns:
            Generated API key and token info
        """
        payload = {
            "provider_id": provider_id,
            "name": name,
            "scopes": scopes,
            "environment": environment,
            "expires_in_days": expires_in_days
        }
        
        if description:
            payload["description"] = description
            
        if ip_restrictions:
            payload["ip_restrictions"] = ip_restrictions
            
        if metadata:
            payload["metadata"] = metadata
        
        try:
            result = self._request("POST", "/auth/keys/generate", data=payload)
            
            # Update key and key_id if successful
            if "key" in result and "token_info" in result and "id" in result["token_info"]:
                self.api_key = result["key"]
                self.key_id = result["token_info"]["id"]
                self.logger.info(f"Successfully generated API key with ID: {self.key_id}")
            
            return result
        except ServerError as e:
            # Enhanced error handling for key generation
            raise KeyGenerationError(
                f"Failed to generate API key: {e.message}. This could be due to server configuration issues or database connectivity.",
                e.status_code, 
                e.response
            )
        except Exception as e:
            # Wrap other exceptions in a KeyGenerationError
            if isinstance(e, AuthAPIError):
                raise KeyGenerationError(
                    f"Failed to generate API key: {e.message}", 
                    getattr(e, 'status_code', None),
                    getattr(e, 'response', None)
                )
            else:
                raise KeyGenerationError(f"Failed to generate API key: {str(e)}")
    
    def list_api_keys(
        self,
        provider_id: Optional[str] = None,
        environment: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        List API keys with optional filtering
        
        Args:
            provider_id: Filter by provider ID
            environment: Filter by environment
            status: Filter by status (active, inactive)
            limit: Maximum number of results
            offset: Result offset for pagination
            
        Returns:
            List of API keys
        """
        params = {"limit": limit, "offset": offset}
        
        if provider_id:
            params["provider_id"] = provider_id
            
        if environment:
            params["environment"] = environment
            
        if status:
            params["status"] = status
            
        return self._request("GET", "/auth/keys", params=params)
    
    def get_key_usage(self, key_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get usage statistics for a specific API key
        
        Args:
            key_id: API key ID. If not provided, uses the current key_id.
            
        Returns:
            Usage statistics
            
        Raises:
            ValidationError: If no key_id is available
        """
        key_id = key_id or self.key_id
        
        if not key_id:
            raise ValidationError("Key ID is required for usage statistics. "
                                 "Either provide a key_id parameter or set it when initializing the client.")
            
        return self._request("GET", f"/auth/keys/{key_id}/usage")
    
    def revoke_api_key(
        self, 
        key_id: Optional[str] = None, 
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Revoke an API key
        
        Args:
            key_id: API key ID to revoke. If not provided, uses the current key_id.
            reason: Optional reason for revocation
            
        Returns:
            Revocation confirmation
            
        Raises:
            ValidationError: If no key_id is available
        """
        key_id = key_id or self.key_id
        
        if not key_id:
            raise ValidationError("Key ID is required for revocation. "
                                 "Either provide a key_id parameter or set it when initializing the client.")
            
        data = {}
        if reason:
            data["reason"] = reason
            
        try:
            result = self._request("POST", f"/auth/keys/{key_id}/revoke", data=data)
        except ClientError as e:
            # If 404, treat as already revoked
            if e.status_code == 404:
                self.logger.info(f"Key {key_id} not found - treating as already revoked")
                result = {"status": "already_revoked", "message": "Key was not found, it may already be revoked"}
            else:
                # Re-raise other client errors
                raise
        
        # If revoking the current key, clear it
        if key_id == self.key_id:
            self.logger.info("Current API key has been revoked, clearing client state")
            self.key_id = None
            self.api_key = None
        
        return result
    
    def update_batch_usage(
        self,
        updates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Update usage statistics for multiple API keys in a batch
        
        Args:
            updates: List of usage update objects
            
        Returns:
            Batch update confirmation
            
        Each update object should have:
        - token_id: API key ID
        - request_count: Number of requests to add
        - last_used: Timestamp of last usage
        - endpoints: Dict mapping endpoint paths to request counts
        - status_codes: Dict mapping status codes to counts
        """
        return self._request(
            "POST", 
            "/auth/keys/batch/usage", 
            data={"updates": updates}
        )
    
    def batch_operations(
        self,
        operation: str,
        key_ids: List[str],
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Perform batch operations on multiple API keys
        
        Args:
            operation: Operation type (update_status, add_metadata, etc.)
            key_ids: List of API key IDs to operate on
            params: Operation parameters
            
        Returns:
            Operation result
        """
        data = {
            "operation": operation,
            "key_ids": key_ids,
            "params": params
        }
        
        return self._request("POST", "/auth/keys/batch/operations", data=data)

    # ----------------------
    # Utility Methods
    # ----------------------
    
    def validate_api_key(self, api_key: str) -> Dict[str, Any]:
        """
        Validate an API key by attempting to access a protected endpoint
        
        Args:
            api_key: API key to validate
            
        Returns:
            Validation result with key details
            
        Raises:
            AuthenticationError: If the key is invalid
        """
        original_key = self.api_key
        original_key_id = self.key_id
        self.api_key = api_key
        self.key_id = None
        
        try:
            result = self.protected_endpoint()
            
            # Try to extract key ID from response
            key_id = None
            if "key_id" in result:
                key_id = result["key_id"]
            elif "token_id" in result:
                key_id = result["token_id"]
                
            return {
                "valid": True,
                "key_id": key_id,
                "provider_id": result.get("provider_id"),
                "scopes": result.get("scopes", []),
                "message": "API key is valid"
            }
        except AuthenticationError:
            return {
                "valid": False,
                "message": "API key is invalid or expired"
            }
        finally:
            self.api_key = original_key
            self.key_id = original_key_id
    
    def set_api_key(self, api_key: str, key_id: Optional[str] = None) -> None:
        """
        Set the API key for subsequent requests
        
        Args:
            api_key: API key to use
            key_id: Optional key ID to associate with this API key
        """
        self.api_key = api_key
        
        if key_id:
            self.key_id = key_id
            self.logger.debug(f"API key and ID have been updated. ID: {self.key_id}")
        else:
            self.key_id = None
            self.logger.debug("API key has been updated, but no ID was provided")
            # Try to fetch the key ID automatically
            try:
                self._fetch_key_id()
            except Exception as e:
                self.logger.warning(f"Could not fetch key ID automatically: {str(e)}")
    
    def create_usage_update(
        self,
        endpoint_path: str,
        status_code: Union[str, int],
        request_count: int = 1,
        timestamp: Optional[str] = None,
        token_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a usage update object for batch usage updates
        
        Args:
            endpoint_path: API endpoint path
            status_code: HTTP status code
            request_count: Number of requests
            timestamp: Optional timestamp (defaults to current time)
            token_id: Optional token ID (defaults to current key_id)
            
        Returns:
            Usage update object ready for batch update
            
        Raises:
            ValidationError: If no token_id is available and none is provided
        """
        status_code = str(status_code)
        token_id = token_id or self.key_id
        
        if not token_id:
            raise ValidationError("Token ID is required for usage updates. "
                                 "Either provide a token_id parameter or set key_id when initializing the client.")
            
        if timestamp is None:
            timestamp = datetime.now(timezone.utc).isoformat()
            
        return {
            "token_id": token_id,
            "request_count": request_count,
            "last_used": timestamp,
            "endpoints": {endpoint_path: request_count},
            "status_codes": {status_code: request_count}
        }

    def get_current_key_info(self) -> Dict[str, Any]:
        """
        Get information about the current API key
        
        Returns:
            Dictionary with key information
            
        Raises:
            ValidationError: If no API key is set
        """
        if not self.api_key:
            raise ValidationError("No API key is currently set")
            
        try:
            # Try to get info from protected endpoint
            result = self.protected_endpoint()
            
            # Enhance with additional details if we have the key ID
            if self.key_id:
                try:
                    usage = self.get_key_usage(self.key_id)
                    result.update({
                        "usage": usage
                    })
                except Exception as e:
                    self.logger.warning(f"Could not fetch usage information: {str(e)}")
            
            return {
                "key_id": self.key_id,
                "is_valid": True,
                "provider_id": result.get("provider_id"),
                "scopes": result.get("scopes", []),
                "details": result
            }
        except AuthenticationError:
            return {
                "key_id": self.key_id,
                "is_valid": False,
                "message": "API key is invalid or expired"
            }
        except Exception as e:
            return {
                "key_id": self.key_id,
                "is_valid": False,
                "message": f"Error validating key: {str(e)}"
            }

# Example usage
if __name__ == "__main__":
    # Create client
    client = AuthAPIClient(base_url="http://localhost:8000")
    
    try:
        # Check if API is healthy
        health = client.health_check()
        print(f"API Health: {health['status']}")
        
        # Generate API key
        key_data = client.generate_api_key(
            provider_id=f"example-provider-{uuid.uuid4().hex[:8]}",
            name="Example Key",
            scopes=["api:access"],
            environment="test",
            expires_in_days=30,
            description="Example key for testing"
        )
        
        print(f"Generated API Key: {key_data['key']}")
        print(f"Key ID: {key_data['token_info']['id']}")
        
        # Set the API key for subsequent requests
        client.set_api_key(key_data['key'], key_data['token_info']['id'])
        
        # Call protected endpoint
        protected = client.protected_endpoint()
        print(f"Protected endpoint response: {protected}")
        
        # Check key usage
        usage = client.get_key_usage()
        print(f"Key usage: {usage}")
        
    except KeyGenerationError as e:
        print(f"Key Generation Error: {e.message}")
        if e.status_code:
            print(f"Status code: {e.status_code}")
        if hasattr(e, 'response') and e.response:
            print(f"Response details: {e.response.text if hasattr(e.response, 'text') else 'Not available'}")
    except AuthAPIError as e:
        print(f"API Error: {e.message} (Status: {e.status_code})") 