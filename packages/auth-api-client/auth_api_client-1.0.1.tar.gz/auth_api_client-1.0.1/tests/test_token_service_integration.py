#!/usr/bin/env python3
"""
Token Service Integration Test
-----------------------------
Tests the complete flow of TokenService operations with SAS token authentication.
This script demonstrates creating, listing, validating, and revoking tokens.

Usage:
  python test_token_service_integration.py

Environment variables required:
  - AZURE_STORAGE_ACCOUNT: Azure Storage account name
  - AZURE_STORAGE_KEY: Azure Storage account key
  - AZURE_STORAGE_CONNECTION_STRING: (Optional) Connection string
  - USE_AZURE_TABLE_STORAGE: Set to "true" to use Table Storage
  - USE_AZURE_SAS_GENERATOR: Set to "true" to use SAS token generator
"""

import os
import sys
import logging
import asyncio
import hashlib
import argparse
from datetime import datetime
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from api_keys.services.token_service import TokenService
from api_keys.services.table_storage import TableStorageClient
from api_keys.services.sas_token_generator import SasTokenGenerator

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_test_environment():
    """Set up the test environment variables if they are not already set."""
    # Only set if not already defined
    if not os.getenv("USE_AZURE_TABLE_STORAGE"):
        os.environ["USE_AZURE_TABLE_STORAGE"] = "true"
    
    if not os.getenv("USE_AZURE_SAS_GENERATOR"):
        os.environ["USE_AZURE_SAS_GENERATOR"] = "true"
    
    if not os.getenv("DB_FALLBACK"):
        os.environ["DB_FALLBACK"] = "true"
    
    # Check for required Azure credentials
    required_vars = ["AZURE_STORAGE_ACCOUNT", "AZURE_STORAGE_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        logger.error(f"Missing required environment variables: {', '.join(missing)}")
        logger.error("Please set these variables before running the test.")
        return False
    
    # Set endpoint if not already defined
    if not os.getenv("AZURE_STORAGE_ENDPOINT"):
        account = os.getenv("AZURE_STORAGE_ACCOUNT")
        os.environ["AZURE_STORAGE_ENDPOINT"] = f"https://{account}.table.core.windows.net"
    
    return True

async def test_token_creation(token_service):
    """Test creating a new token."""
    logger.info("Testing token creation...")
    
    # Create a token for testing
    provider_id = f"test-provider-{int(time.time())}"
    token_name = f"Test Token {datetime.utcnow().isoformat()}"
    
    token_data, raw_token = await token_service.create_token(
        provider_id=provider_id,
        name=token_name,
        scopes=["read", "write", "admin"],
        environment="test",
        expires_in_days=1,  # Short expiry for testing
        description="Integration test token",
        ip_restrictions=None
    )
    
    if not token_data or not raw_token:
        logger.error("Failed to create token")
        return None, None
    
    logger.info(f"Token created successfully: {token_data['id']}")
    logger.info(f"Raw token: {raw_token}")
    
    # Hash the raw token for future validation tests
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    
    return token_data, token_hash

async def test_token_listing(token_service, provider_id):
    """Test listing tokens for a provider."""
    logger.info(f"Testing token listing for provider {provider_id}...")
    
    tokens = await token_service.list_tokens(provider_id)
    
    if not tokens:
        logger.error(f"No tokens found for provider {provider_id}")
        return False
    
    logger.info(f"Found {len(tokens)} tokens for provider {provider_id}")
    for token in tokens:
        logger.info(f"  - {token['id']}: {token['name']} ({token['status']})")
    
    return True

async def test_token_validation(token_service, token_hash):
    """Test validating a token."""
    logger.info(f"Testing token validation...")
    
    validation = await token_service.validate_token(token_hash)
    
    if not validation or not validation.get("valid"):
        logger.error(f"Token validation failed: {validation.get('reason', 'Unknown error')}")
        return False
    
    logger.info(f"Token validated successfully for provider {validation['provider_id']}")
    logger.info(f"Token scopes: {validation['scopes']}")
    
    return True

async def test_token_usage(token_service, token_id):
    """Test logging and retrieving token usage."""
    logger.info(f"Testing token usage logging...")
    
    # Log some usage
    await token_service.log_token_usage(
        token_id=token_id,
        endpoint="/api/test",
        status_code=200
    )
    
    await token_service.log_token_usage(
        token_id=token_id,
        endpoint="/api/data",
        status_code=201
    )
    
    # Log an error
    await token_service.log_token_usage(
        token_id=token_id,
        endpoint="/api/protected",
        status_code=403,
        error="Permission denied"
    )
    
    # Get usage statistics
    usage = await token_service.get_api_key_usage(token_id)
    
    if not usage:
        logger.error("Failed to retrieve token usage")
        return False
    
    logger.info(f"Token usage retrieved successfully:")
    logger.info(f"  - Request count: {usage['request_count']}")
    logger.info(f"  - Endpoints: {usage['endpoints']}")
    logger.info(f"  - Status codes: {usage['status_codes']}")
    logger.info(f"  - Errors: {len(usage['errors'])}")
    
    return True

async def test_token_revocation(token_service, token_id):
    """Test revoking a token."""
    logger.info(f"Testing token revocation...")
    
    revocation = await token_service.revoke_token(
        token_id=token_id,
        reason="Integration test completion"
    )
    
    if not revocation:
        logger.error("Failed to revoke token")
        return False
    
    logger.info(f"Token revoked successfully with reason: {revocation['revocation_reason']}")
    
    # Verify the token is revoked
    is_revoked = await token_service.is_token_revoked(token_id)
    
    if not is_revoked:
        logger.error(f"Token {token_id} should be revoked but isn't")
        return False
        
    logger.info(f"Token revocation status confirmed")
    return True

async def run_token_service_tests():
    """Run the complete token service test flow."""
    logger.info("Starting Token Service integration tests")
    
    # Set up test environment
    if not setup_test_environment():
        return 1
    
    # Initialize token service
    token_service = TokenService()
    await token_service.init()
    
    if not token_service.table_storage or not token_service.table_storage._initialized:
        logger.error("Failed to initialize Token Service with Table Storage")
        return 1
    
    logger.info("Token Service initialized successfully with Table Storage")
    
    # Test creating a token
    token_data, token_hash = await test_token_creation(token_service)
    if not token_data:
        return 1
    
    provider_id = token_data["provider_id"]
    token_id = token_data["id"]
    
    # Test listing tokens
    if not await test_token_listing(token_service, provider_id):
        return 1
    
    # Test validating a token
    if not await test_token_validation(token_service, token_hash):
        return 1
    
    # Test token usage logging and retrieval
    if not await test_token_usage(token_service, token_id):
        return 1
    
    # Test revoking a token
    if not await test_token_revocation(token_service, token_id):
        return 1
    
    logger.info("All Token Service tests completed successfully")
    return 0

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Test Token Service integration with SAS authentication")
    
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Run cleanup operations (delete test tables)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    return parser.parse_args()

async def cleanup_test_resources():
    """Clean up any test resources created during tests."""
    logger.info("Cleaning up test resources...")
    
    if not setup_test_environment():
        return False
    
    try:
        # Initialize Table Storage client
        storage_client = TableStorageClient(
            endpoint=os.getenv("AZURE_STORAGE_ENDPOINT"),
            use_sas_generator=True
        )
        
        if not storage_client.initialize():
            logger.error("Failed to initialize Table Storage client for cleanup")
            return False
        
        # List tables that could have been created by tests
        if storage_client.table_service:
            tables = storage_client.table_service.list_tables()
            test_tables = [table.name for table in tables if table.name.startswith(("Test", "test"))]
            
            if test_tables:
                logger.info(f"Found {len(test_tables)} test tables to clean up")
                for table_name in test_tables:
                    logger.info(f"Deleting table: {table_name}")
                    storage_client.delete_table(table_name)
            else:
                logger.info("No test tables found to clean up")
        
        logger.info("Cleanup completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")
        return False

def main():
    """Main function."""
    args = parse_args()
    
    # Set log level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Run cleanup if requested
    if args.cleanup:
        return asyncio.run(cleanup_test_resources())
    
    # Run the token service tests
    return asyncio.run(run_token_service_tests())

if __name__ == "__main__":
    sys.exit(main()) 