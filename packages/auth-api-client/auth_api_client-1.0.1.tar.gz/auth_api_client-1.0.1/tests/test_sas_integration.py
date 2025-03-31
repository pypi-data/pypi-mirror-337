#!/usr/bin/env python3
"""
SAS Token Integration Test
-------------------------
A test script to verify SAS token generation and Table Storage integration.
This script can be run directly to test against real Azure services.

Usage:
  python test_sas_integration.py 

Environment variables required:
  - AZURE_STORAGE_ACCOUNT: Azure Storage account name
  - AZURE_STORAGE_KEY: Azure Storage account key
  - AZURE_STORAGE_CONNECTION_STRING: (Optional) Connection string

The script will:
1. Generate a SAS token using the SAS token generator
2. Initialize a Table Storage client with the token
3. Create a test table
4. Add a test entity
5. Retrieve the entity
6. Delete the entity and table
"""

import os
import sys
import logging
import uuid
import time
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from api_keys.services.sas_token_generator import SasTokenGenerator
from api_keys.services.table_storage import TableStorageClient

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_environment():
    """Check if required environment variables are set."""
    required_vars = ["AZURE_STORAGE_ACCOUNT", "AZURE_STORAGE_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        logger.error(f"Missing required environment variables: {', '.join(missing)}")
        logger.error("Please set these variables before running the test.")
        return False
    return True

def test_sas_token_generation():
    """Test generating a SAS token."""
    logger.info("Testing SAS token generation...")
    
    generator = SasTokenGenerator()
    
    # Get the Azure Storage endpoint
    endpoint = generator.get_account_endpoint("table")
    logger.info(f"Azure Storage endpoint: {endpoint}")
    
    # Generate a SAS token for table storage
    token = generator.generate_table_sas(
        expiry_hours=1,  # Short-lived token for testing
        permissions="raud"  # read, add, update, delete
    )
    
    if not token:
        logger.error("Failed to generate SAS token")
        return None, None
    
    logger.info(f"SAS token generated successfully: {token[:20]}...")
    return endpoint, token

def test_table_storage_with_sas(endpoint, sas_token):
    """Test table storage operations using SAS token."""
    if not endpoint or not sas_token:
        logger.error("Cannot test Table Storage without endpoint and SAS token")
        return False
    
    # Create a test table name with timestamp to avoid conflicts
    test_table = f"TestSasToken{int(time.time())}"
    
    logger.info(f"Testing Table Storage with SAS token using table: {test_table}")
    
    # Initialize Table Storage client with SAS token
    storage_client = TableStorageClient(
        endpoint=endpoint,
        sas_token=sas_token,
        table_names=[test_table]
    )
    
    # Initialize the client
    if not storage_client.initialize():
        logger.error("Failed to initialize Table Storage client")
        return False
    
    # Generate a unique ID for the test entity
    entity_id = str(uuid.uuid4())
    test_data = "Test data " + datetime.utcnow().isoformat()
    
    try:
        # Create test entity
        logger.info("Creating test entity...")
        entity = {
            "PartitionKey": "TestPartition",
            "RowKey": entity_id,
            "TestData": test_data,
            "CreatedAt": datetime.utcnow().isoformat()
        }
        
        if not storage_client.create_entity(test_table, entity):
            logger.error("Failed to create test entity")
            return False
        
        logger.info("Test entity created successfully")
        
        # Retrieve the entity
        logger.info("Retrieving test entity...")
        retrieved = storage_client.get_entity(test_table, "TestPartition", entity_id)
        
        if not retrieved:
            logger.error("Failed to retrieve test entity")
            return False
        
        # Verify the data
        if retrieved.get("TestData") != test_data:
            logger.error(f"Data mismatch: {retrieved.get('TestData')} != {test_data}")
            return False
            
        logger.info("Retrieved entity matches test data")
        
        # Update the entity
        logger.info("Updating test entity...")
        retrieved["TestData"] = "Updated " + test_data
        
        if not storage_client.update_entity(test_table, retrieved):
            logger.error("Failed to update test entity")
            return False
            
        # Verify update
        updated = storage_client.get_entity(test_table, "TestPartition", entity_id)
        if not updated or updated.get("TestData") != "Updated " + test_data:
            logger.error("Update verification failed")
            return False
            
        logger.info("Entity updated successfully")
        
        # Delete the entity
        logger.info("Deleting test entity...")
        if not storage_client.delete_entity(test_table, "TestPartition", entity_id):
            logger.error("Failed to delete test entity")
            
        # Delete the test table
        logger.info("Deleting test table...")
        storage_client.delete_table(test_table)
        
        logger.info("Table Storage test completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error during Table Storage test: {str(e)}")
        # Clean up by deleting the table
        try:
            storage_client.delete_table(test_table)
        except:
            pass
        return False

def test_table_storage_with_generator():
    """Test table storage with SAS token generator."""
    logger.info("Testing Table Storage with SAS token generator...")
    
    # Create a test table name with timestamp to avoid conflicts
    test_table = f"TestSasGen{int(time.time())}"
    
    # Initialize Table Storage client with SAS generator
    storage_client = TableStorageClient(
        table_names=[test_table],
        use_sas_generator=True
    )
    
    # Initialize the client
    if not storage_client.initialize():
        logger.error("Failed to initialize Table Storage client with SAS generator")
        return False
    
    # Generate a unique ID for the test entity
    entity_id = str(uuid.uuid4())
    test_data = "Generator test " + datetime.utcnow().isoformat()
    
    try:
        # Create test entity
        logger.info("Creating test entity with generated SAS token...")
        entity = {
            "PartitionKey": "GeneratorTest",
            "RowKey": entity_id,
            "TestData": test_data,
            "CreatedAt": datetime.utcnow().isoformat()
        }
        
        if not storage_client.create_entity(test_table, entity):
            logger.error("Failed to create test entity with generated token")
            return False
        
        logger.info("Test entity created successfully with generated token")
        
        # Clean up
        storage_client.delete_entity(test_table, "GeneratorTest", entity_id)
        storage_client.delete_table(test_table)
        
        logger.info("SAS token generator test completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error during SAS generator test: {str(e)}")
        # Clean up
        try:
            storage_client.delete_table(test_table)
        except:
            pass
        return False

def main():
    """Main function to run the integration tests."""
    logger.info("Starting SAS token integration tests")
    
    # Check environment variables
    if not check_environment():
        return 1
    
    # Test SAS token generation
    endpoint, token = test_sas_token_generation()
    if not token:
        return 1
    
    # Test Table Storage with SAS token
    if not test_table_storage_with_sas(endpoint, token):
        return 1
    
    # Test Table Storage with SAS token generator
    if not test_table_storage_with_generator():
        return 1
    
    logger.info("All tests completed successfully")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 