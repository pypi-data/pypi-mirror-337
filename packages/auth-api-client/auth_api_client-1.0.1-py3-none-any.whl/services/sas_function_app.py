"""
Azure Function App for SAS Token Generation
------------------------------------------
This module provides the Azure Function App implementation for generating SAS tokens.
It serves as the primary method for token generation in our hybrid approach.

This can be deployed as an Azure Function, providing centralized and secure token generation.
"""

import os
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, Any, List, Union, Tuple

import azure.functions as func
from azure.core.credentials import AzureNamedKeyCredential
from azure.data.tables import generate_table_sas, TableSasPermissions
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from azure.storage.queue import generate_queue_sas, QueueSasPermissions

# Configure logging
logger = logging.getLogger("sas_function_app")

# Environment variable keys
ENV_FRONTDOOR_ID = "AZURE_FRONTDOOR_ID"
ENV_FUNCTION_KEY = "AZURE_FUNCTION_KEY"

def extract_storage_credentials(req: func.HttpRequest) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Extract storage credentials from request.
    
    Args:
        req: The HTTP request
        
    Returns:
        Tuple of (connection_string, account_name, account_key)
    """
    connection_string = req.params.get("connectionString")
    account_name = req.params.get("accountName")
    account_key = req.params.get("accountKey")
    
    # Validate we have either connection string OR account credentials
    if connection_string:
        return connection_string, None, None
    elif account_name and account_key:
        return None, account_name, account_key
    else:
        return None, None, None

def validate_frontdoor(req: func.HttpRequest) -> bool:
    """Validate request is coming through Azure Front Door.
    
    Args:
        req: The HTTP request
        
    Returns:
        True if validation passes, False otherwise
    """
    # Get expected Front Door ID from environment
    expected_fd_id = os.environ.get(ENV_FRONTDOOR_ID)
    if not expected_fd_id:
        # If no Front Door ID is configured, skip validation
        logger.warning("No Front Door ID configured, skipping validation")
        return True
        
    # Get Front Door ID from request
    fd_id = req.params.get("frontDoorId")
    if not fd_id:
        logger.warning("No Front Door ID in request")
        return False
        
    # Validate
    return fd_id == expected_fd_id

def validate_function_key(req: func.HttpRequest) -> bool:
    """Validate function key in request.
    
    Args:
        req: The HTTP request
        
    Returns:
        True if validation passes, False otherwise
    """
    # Get expected key from environment
    expected_key = os.environ.get(ENV_FUNCTION_KEY)
    if not expected_key:
        # If no key is configured, fail validation
        logger.warning("No function key configured")
        return False
        
    # Get key from request (typically in 'code' parameter)
    key = req.params.get("code")
    if not key:
        logger.warning("No function key in request")
        return False
        
    # Validate
    return key == expected_key

def generate_table_sas_token(
    req: func.HttpRequest,
    connection_string: Optional[str] = None,
    account_name: Optional[str] = None,
    account_key: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Generate SAS token for Table Storage.
    
    Args:
        req: The HTTP request
        connection_string: Optional connection string
        account_name: Optional account name
        account_key: Optional account key
        
    Returns:
        Dictionary with SAS token and expiry, or None if generation failed
    """
    try:
        # Get parameters
        expiry_hours = int(req.params.get("expiry", "24"))
        permissions = req.params.get("permissions", "r")
        table_name = req.params.get("resourceName", "")
        protocol = req.params.get("protocol", "https")
        
        # Ensure permissions are in the correct order for table storage
        # The correct order for table storage is: raud (Read/Query, Add, Update, Delete)
        sorted_permissions = ""
        if 'r' in permissions:
            sorted_permissions += 'r'  # Read/Query operations
        if 'a' in permissions:
            sorted_permissions += 'a'  # Add operations
        if 'u' in permissions:
            sorted_permissions += 'u'  # Update operations
        if 'd' in permissions:
            sorted_permissions += 'd'  # Delete operations
            
        # Calculate expiry time
        expiry = datetime.utcnow() + timedelta(hours=expiry_hours)
        
        # Generate SAS token
        if connection_string:
            # Extract account name and key from connection string
            parts = connection_string.split(';')
            for part in parts:
                if part.startswith('AccountName='):
                    account_name = part.split('=', 1)[1]
                elif part.startswith('AccountKey='):
                    account_key = part.split('=', 1)[1]
        
        if not (account_name and account_key):
            logger.error("Missing account credentials")
            return None
            
        # Create credential with Azure SDK
        credential = AzureNamedKeyCredential(account_name, account_key)
        
        # Create permission object
        table_permission = TableSasPermissions(
            read='r' in sorted_permissions,
            add='a' in sorted_permissions,
            update='u' in sorted_permissions,
            delete='d' in sorted_permissions
        )
        
        # Generate SAS token
        sas_token = generate_table_sas(
            credential=credential,
            table_name=table_name,
            permission=table_permission,
            expiry=expiry,
            protocol=protocol
        )
        
        logger.info(f"Successfully generated table SAS token for {account_name}")
        return {
            "sasToken": sas_token,
            "expiresOn": expiry.isoformat() + "Z",
            "permissions": sorted_permissions
        }
        
    except Exception as e:
        logger.error(f"Failed to generate table SAS token: {str(e)}")
        return None

def generate_blob_sas_token(
    req: func.HttpRequest,
    connection_string: Optional[str] = None,
    account_name: Optional[str] = None,
    account_key: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Generate SAS token for Blob Storage.
    
    Args:
        req: The HTTP request
        connection_string: Optional connection string
        account_name: Optional account name
        account_key: Optional account key
        
    Returns:
        Dictionary with SAS token and expiry, or None if generation failed
    """
    try:
        # Get parameters
        expiry_hours = int(req.params.get("expiry", "24"))
        permissions = req.params.get("permissions", "r")
        resource_name = req.params.get("resourceName", "")
        protocol = req.params.get("protocol", "https")
        
        # Parse container and blob name from resource_name
        container_name = resource_name
        blob_name = None
        if resource_name and '/' in resource_name:
            parts = resource_name.split('/', 1)
            container_name = parts[0]
            blob_name = parts[1] if len(parts) > 1 else None
        
        # Calculate expiry time
        expiry = datetime.utcnow() + timedelta(hours=expiry_hours)
        
        # Generate SAS token
        if connection_string:
            # Extract account name and key from connection string
            parts = connection_string.split(';')
            for part in parts:
                if part.startswith('AccountName='):
                    account_name = part.split('=', 1)[1]
                elif part.startswith('AccountKey='):
                    account_key = part.split('=', 1)[1]
        
        if not (account_name and account_key):
            logger.error("Missing account credentials")
            return None
        
        # Generate SAS token
        sas_token = generate_blob_sas(
            account_name=account_name,
            account_key=account_key,
            container_name=container_name,
            blob_name=blob_name,
            permission=BlobSasPermissions(
                read='r' in permissions,
                add='a' in permissions,
                create='c' in permissions,
                write='w' in permissions,
                delete='d' in permissions,
                tag='t' in permissions,
                list='l' in permissions,
                move='m' in permissions,
                execute='e' in permissions,
                set_immutability_policy='i' in permissions,
                permanent_delete='p' in permissions,
                filter_by_tags='f' in permissions
            ),
            expiry=expiry,
            protocol=protocol
        )
        
        logger.info(f"Successfully generated blob SAS token for {account_name}")
        return {
            "sasToken": sas_token,
            "expiresOn": expiry.isoformat() + "Z",
            "permissions": permissions
        }
        
    except Exception as e:
        logger.error(f"Failed to generate blob SAS token: {str(e)}")
        return None

def generate_queue_sas_token(
    req: func.HttpRequest,
    connection_string: Optional[str] = None,
    account_name: Optional[str] = None,
    account_key: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Generate SAS token for Queue Storage.
    
    Args:
        req: The HTTP request
        connection_string: Optional connection string
        account_name: Optional account name
        account_key: Optional account key
        
    Returns:
        Dictionary with SAS token and expiry, or None if generation failed
    """
    try:
        # Get parameters
        expiry_hours = int(req.params.get("expiry", "24"))
        permissions = req.params.get("permissions", "raup")
        queue_name = req.params.get("resourceName", "")
        protocol = req.params.get("protocol", "https")
        
        # Calculate expiry time
        expiry = datetime.utcnow() + timedelta(hours=expiry_hours)
        
        # Generate SAS token
        if connection_string:
            # Extract account name and key from connection string
            parts = connection_string.split(';')
            for part in parts:
                if part.startswith('AccountName='):
                    account_name = part.split('=', 1)[1]
                elif part.startswith('AccountKey='):
                    account_key = part.split('=', 1)[1]
        
        if not (account_name and account_key):
            logger.error("Missing account credentials")
            return None
        
        # Generate SAS token
        sas_token = generate_queue_sas(
            account_name=account_name,
            account_key=account_key,
            queue_name=queue_name,
            permission=QueueSasPermissions(
                read='r' in permissions,
                add='a' in permissions,
                update='u' in permissions,
                process='p' in permissions
            ),
            expiry=expiry,
            protocol=protocol
        )
        
        logger.info(f"Successfully generated queue SAS token for {account_name}")
        return {
            "sasToken": sas_token,
            "expiresOn": expiry.isoformat() + "Z",
            "permissions": permissions
        }
        
    except Exception as e:
        logger.error(f"Failed to generate queue SAS token: {str(e)}")
        return None

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Azure Function entry point for SAS token generation.
    
    Args:
        req: The HTTP request
        
    Returns:
        HTTP response with SAS token or error message
    """
    logger.info("SAS Generator Function called")
    
    # Validate Front Door and function key
    if not validate_frontdoor(req):
        return func.HttpResponse(
            body=json.dumps({"error": "Unauthorized request - Front Door validation failed"}),
            status_code=403,
            mimetype="application/json"
        )
        
    if not validate_function_key(req):
        return func.HttpResponse(
            body=json.dumps({"error": "Unauthorized request - Invalid function key"}),
            status_code=401,
            mimetype="application/json"
        )
    
    # Extract storage credentials
    connection_string, account_name, account_key = extract_storage_credentials(req)
    
    # Validate we have credentials
    if not (connection_string or (account_name and account_key)):
        return func.HttpResponse(
            body=json.dumps({
                "error": "Missing storage account credentials",
                "message": "Provide either connectionString or accountName+accountKey"
            }),
            status_code=400,
            mimetype="application/json"
        )
    
    # Get resource type (table, blob, queue)
    resource_type = req.params.get("resourceType", "").lower()
    if not resource_type:
        return func.HttpResponse(
            body=json.dumps({"error": "Missing resourceType parameter"}),
            status_code=400,
            mimetype="application/json"
        )
    
    # Generate SAS token based on resource type
    result = None
    if resource_type == "table":
        result = generate_table_sas_token(req, connection_string, account_name, account_key)
    elif resource_type == "blob":
        result = generate_blob_sas_token(req, connection_string, account_name, account_key)
    elif resource_type == "queue":
        result = generate_queue_sas_token(req, connection_string, account_name, account_key)
    else:
        return func.HttpResponse(
            body=json.dumps({"error": f"Unsupported resource type: {resource_type}"}),
            status_code=400,
            mimetype="application/json"
        )
    
    # Return result
    if result:
        return func.HttpResponse(
            body=json.dumps(result),
            status_code=200,
            mimetype="application/json"
        )
    else:
        return func.HttpResponse(
            body=json.dumps({"error": f"Failed to generate SAS token for {resource_type}"}),
            status_code=500,
            mimetype="application/json"
        ) 