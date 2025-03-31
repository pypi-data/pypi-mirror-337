"""
SAS Token Generator for Azure Storage.

This module provides a SasTokenGenerator class that handles SAS token generation
for Azure Storage services with rate limiting and fallback mechanisms.
"""

import logging
import time
import datetime
import urllib.parse
import hmac
import hashlib
import base64
from typing import Optional, Dict, Any, Tuple

from azure.data.tables import generate_account_sas, ResourceTypes, AccountSasPermissions
from azure.core.exceptions import HttpResponseError

logger = logging.getLogger(__name__)

class SasTokenGenerator:
    """
    Generates SAS tokens for Azure Storage with rate limiting and fallback capability.
    
    This class provides methods to generate SAS tokens for Azure Storage services,
    with built-in rate limiting to prevent exceeding Azure API quotas. If the primary
    method using the Azure SDK exceeds rate limits, it will fall back to a manual
    implementation.
    
    Attributes:
        account_name (str): The Azure Storage account name.
        account_key (str): The Azure Storage account key.
        max_requests (int): Maximum number of requests allowed in the time window.
        window_ms (int): Time window in milliseconds for rate limiting.
        requests (list): List of timestamps of recent requests.
        _last_token_expiry (int): Expiration time of the last generated token.
        _enable_fallback (bool): Whether to enable fallback to manual implementation.
    """

    def __init__(
        self,
        account_name: str,
        account_key: str,
        max_requests: int = 100,
        window_ms: int = 60000,
        enable_fallback: bool = True,
    ):
        """
        Initialize the SAS token generator.
        
        Args:
            account_name: Azure Storage account name.
            account_key: Azure Storage account key.
            max_requests: Maximum number of requests allowed in the window.
            window_ms: Time window in milliseconds for rate limiting.
            enable_fallback: Whether to enable fallback to manual implementation.
        """
        self.account_name = account_name
        self.account_key = account_key
        self.max_requests = max_requests
        self.window_ms = window_ms
        self.requests = []
        self._last_token_expiry = 0
        self._enable_fallback = enable_fallback
        self._fallback_triggered = False
        logger.info(
            f"Initialized SasTokenGenerator for account '{account_name}' "
            f"with rate limit of {max_requests} requests per {window_ms}ms "
            f"and fallback {'enabled' if enable_fallback else 'disabled'}"
        )

    def _is_rate_limited(self) -> bool:
        """
        Check if the current request would exceed the rate limit.
        
        Returns:
            bool: True if rate limited, False otherwise.
        """
        now = int(time.time() * 1000)
        # Remove requests outside the window
        self.requests = [req for req in self.requests if now - req < self.window_ms]
        # Check if adding a request would exceed the limit
        return len(self.requests) >= self.max_requests

    def _track_request(self) -> None:
        """Track a new request for rate limiting purposes."""
        now = int(time.time() * 1000)
        self.requests.append(now)

    def generate_table_sas(
        self,
        expiry_minutes: int = 60,
        permissions: Optional[AccountSasPermissions] = None,
    ) -> Tuple[Optional[str], Optional[int]]:
        """
        Generate a SAS token for Azure Table Storage.
        
        Args:
            expiry_minutes: Token expiration time in minutes.
            permissions: Specific permissions for the SAS token.
            
        Returns:
            tuple: (sas_token, expiry_timestamp) or (None, None) if generation fails.
        """
        # Check if we're rate limited and should use fallback
        if self._is_rate_limited() and self._enable_fallback:
            logger.warning(
                "Rate limit exceeded. Falling back to manual SAS token generation."
            )
            self._fallback_triggered = True
            return self._generate_sas_manual(expiry_minutes, permissions)

        # Track this request
        self._track_request()

        try:
            # Use Azure SDK for primary method
            return self._generate_sas_sdk(expiry_minutes, permissions)
        except HttpResponseError as e:
            if e.status_code == 429 and self._enable_fallback:  # Too Many Requests
                logger.warning(
                    f"Received 429 from Azure API. Falling back to manual SAS token generation. Error: {str(e)}"
                )
                self._fallback_triggered = True
                return self._generate_sas_manual(expiry_minutes, permissions)
            logger.error(f"Failed to generate SAS token: {str(e)}")
            return None, None
        except Exception as e:
            logger.error(f"Unexpected error generating SAS token: {str(e)}")
            return None, None

    def _generate_sas_sdk(
        self,
        expiry_minutes: int = 60,
        permissions: Optional[AccountSasPermissions] = None,
    ) -> Tuple[Optional[str], Optional[int]]:
        """
        Generate SAS token using the Azure SDK.
        
        Args:
            expiry_minutes: Token expiration time in minutes.
            permissions: Specific permissions for the SAS token.
            
        Returns:
            tuple: (sas_token, expiry_timestamp) or (None, None) if generation fails.
        """
        try:
            if permissions is None:
                permissions = AccountSasPermissions(read=True, write=True, list=True)

            # Set start and expiry time
            start_time = datetime.datetime.now(datetime.timezone.utc)
            expiry_time = start_time + datetime.timedelta(minutes=expiry_minutes)
            
            # Generate the SAS token
            sas_token = generate_account_sas(
                account_name=self.account_name,
                account_key=self.account_key,
                resource_types=ResourceTypes(service=True, container=True, object=True),
                permission=permissions,
                expiry=expiry_time,
                start=start_time,
            )
            
            expiry_timestamp = int(expiry_time.timestamp())
            self._last_token_expiry = expiry_timestamp
            
            logger.debug(
                f"Generated SAS token using SDK with expiry at {expiry_time.isoformat()}"
            )
            
            return sas_token, expiry_timestamp
        except Exception as e:
            logger.error(f"Error in _generate_sas_sdk: {str(e)}")
            return None, None

    def _generate_sas_manual(
        self,
        expiry_minutes: int = 60,
        permissions: Optional[AccountSasPermissions] = None,
    ) -> Tuple[Optional[str], Optional[int]]:
        """
        Generate SAS token manually as a fallback.
        
        Args:
            expiry_minutes: Token expiration time in minutes.
            permissions: Specific permissions for the SAS token.
            
        Returns:
            tuple: (sas_token, expiry_timestamp) or (None, None) if generation fails.
        """
        try:
            # Set start and expiry time
            start_time = datetime.datetime.now(datetime.timezone.utc)
            expiry_time = start_time + datetime.timedelta(minutes=expiry_minutes)
            
            # Format timestamps as required by Azure
            start_str = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            expiry_str = expiry_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            
            # Define permissions
            perm_str = "rw"  # Default read/write
            if permissions:
                perm_str = ""
                if permissions.read:
                    perm_str += "r"
                if permissions.write:
                    perm_str += "w"
                if permissions.delete:
                    perm_str += "d"
                if permissions.list:
                    perm_str += "l"
                if hasattr(permissions, "process") and permissions.process:
                    perm_str += "p"
            
            # Create the string to sign
            resource_types = "sco"  # Service, Container, Object
            to_sign = "\n".join([
                self.account_name,
                perm_str,
                "sco",  # Resource types
                start_str,
                expiry_str,
                "",  # IP range (blank means all)
                "https,http",  # Protocols
                "2019-12-12",  # API version
            ])
            
            # Generate the signature
            key = base64.b64decode(self.account_key)
            signature = base64.b64encode(
                hmac.new(key, to_sign.encode("utf-8"), hashlib.sha256).digest()
            ).decode("utf-8")
            
            # Construct the SAS token
            sas_params = {
                "sv": "2019-12-12",
                "ss": "t",  # Table service
                "srt": resource_types,
                "sp": perm_str,
                "se": expiry_str,
                "st": start_str,
                "spr": "https,http",
                "sig": signature,
            }
            
            sas_token = "&".join([f"{k}={urllib.parse.quote(v)}" for k, v in sas_params.items()])
            
            expiry_timestamp = int(expiry_time.timestamp())
            self._last_token_expiry = expiry_timestamp
            
            logger.debug(
                f"Generated SAS token manually with expiry at {expiry_time.isoformat()}"
            )
            
            return sas_token, expiry_timestamp
        except Exception as e:
            logger.error(f"Error in _generate_sas_manual: {str(e)}")
            return None, None

    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the SAS token generator.
        
        Returns:
            Dict containing status information including:
            - account_name: The account name being used
            - rate_limit: Configuration details about rate limiting
            - current_usage: Current usage within the rate limit window
            - fallback_status: Information about fallback mechanism
        """
        now = int(time.time() * 1000)
        # Clean up old requests
        self.requests = [req for req in self.requests if now - req < self.window_ms]
        
        return {
            "account_name": self.account_name,
            "rate_limit": {
                "max_requests": self.max_requests,
                "window_ms": self.window_ms,
            },
            "current_usage": {
                "requests_in_window": len(self.requests),
                "rate_limited": self._is_rate_limited()
            },
            "fallback_status": {
                "enabled": self._enable_fallback,
                "triggered": self._fallback_triggered
            },
            "last_token_expiry": self._last_token_expiry
        } 