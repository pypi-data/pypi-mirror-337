#!/usr/bin/env python3
"""
Standalone SAS Token Test Runner
-------------------------------
This script runs the SAS token integration tests directly, 
bypassing the problematic imports in the package's __init__.py file.
"""

import os
import sys
import unittest
from unittest import mock
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import directly from the service modules to avoid __init__.py issues
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from api_keys.services.sas_token_generator import SasTokenGenerator
from api_keys.services.table_storage import TableStorageClient

class TestSasTokenGenerator(unittest.TestCase):
    """Test cases for SAS token generator."""
    
    def setUp(self):
        """Set up test environment."""
        # Mock environment variables
        self.env_patcher = mock.patch.dict(os.environ, {
            "AZURE_STORAGE_ACCOUNT": "teststorageaccount",
            "AZURE_STORAGE_KEY": "test_key_value_1234567890==",
            "AZURE_STORAGE_CONNECTION_STRING": "DefaultEndpointsProtocol=https;AccountName=teststorageaccount;AccountKey=test_key_value_1234567890==;EndpointSuffix=core.windows.net",
        })
        self.env_patcher.start()
        
        # Create test objects
        self.generator = SasTokenGenerator()
        
        # Mock the urllib.request.urlopen to prevent actual HTTP requests
        self.urlopen_patcher = mock.patch('urllib.request.urlopen')
        self.mock_urlopen = self.urlopen_patcher.start()
        
        # Set up mock response for urlopen
        self.mock_response = mock.MagicMock()
        self.mock_response.status = 200
        self.mock_response.__enter__.return_value = self.mock_response
        self.mock_response.read.return_value = json.dumps({
            "sasToken": "sv=2020-10-02&ss=t&srt=o&sp=rwdlacu&se=2023-06-30T05:11:22Z&st=2023-06-29T21:11:22Z&spr=https&sig=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmn%3D",
            "expiresOn": (datetime.utcnow().isoformat() + "Z")
        }).encode('utf-8')
        self.mock_urlopen.return_value = self.mock_response
    
    def tearDown(self):
        """Clean up after tests."""
        self.env_patcher.stop()
        self.urlopen_patcher.stop()
    
    def test_initialization(self):
        """Test that generator initializes correctly from environment variables."""
        logger.info("Testing initialization...")
        self.assertEqual(self.generator.account_name, "teststorageaccount")
        self.assertEqual(self.generator.account_key, "test_key_value_1234567890==")
        self.assertIsNotNone(self.generator.connection_string)
        logger.info("Initialization test passed")
        
    def test_get_account_endpoint(self):
        """Test getting the correct endpoint URL."""
        logger.info("Testing endpoint URL generation...")
        # Test for each resource type
        table_endpoint = self.generator.get_account_endpoint("table")
        self.assertEqual(table_endpoint, "https://teststorageaccount.table.core.windows.net")
        
        blob_endpoint = self.generator.get_account_endpoint("blob")
        self.assertEqual(blob_endpoint, "https://teststorageaccount.blob.core.windows.net")
        
        queue_endpoint = self.generator.get_account_endpoint("queue")
        self.assertEqual(queue_endpoint, "https://teststorageaccount.queue.core.windows.net")
        logger.info("Endpoint URL tests passed")
    
    def test_generate_table_sas(self):
        """Test generating SAS token for table storage."""
        logger.info("Testing table SAS token generation...")
        token = self.generator.generate_table_sas(
            expiry_hours=24,
            permissions="raud",
            table_name="TestTable"
        )
        
        # Verify that token is generated and has expected format
        self.assertIsNotNone(token)
        self.assertIn("sv=", token)
        self.assertIn("sig=", token)
        
        # Check that request was made with correct parameters
        args, kwargs = self.mock_urlopen.call_args
        url = args[0].full_url
        self.assertIn("resourceType=table", url)
        self.assertIn("expiry=24", url)
        self.assertIn("permissions=raud", url)
        self.assertIn("resourceName=TestTable", url)
        logger.info("Table SAS token test passed")
    
    def test_generate_blob_sas(self):
        """Test generating SAS token for blob storage."""
        logger.info("Testing blob SAS token generation...")
        token = self.generator.generate_blob_sas(
            expiry_hours=48,
            permissions="r",
            container_name="testcontainer",
            blob_name="testblob.txt"
        )
        
        # Verify token
        self.assertIsNotNone(token)
        
        # Check request parameters
        args, kwargs = self.mock_urlopen.call_args
        url = args[0].full_url
        self.assertIn("resourceType=blob", url)
        self.assertIn("expiry=48", url)
        self.assertIn("permissions=r", url)
        self.assertIn("resourceName=testcontainer/testblob.txt", url)
        logger.info("Blob SAS token test passed")
    
    def test_generate_queue_sas(self):
        """Test generating SAS token for queue storage."""
        logger.info("Testing queue SAS token generation...")
        token = self.generator.generate_queue_sas(
            expiry_hours=12,
            permissions="raup",
            queue_name="testqueue"
        )
        
        # Verify token
        self.assertIsNotNone(token)
        
        # Check request parameters
        args, kwargs = self.mock_urlopen.call_args
        url = args[0].full_url
        self.assertIn("resourceType=queue", url)
        self.assertIn("expiry=12", url)
        self.assertIn("permissions=raup", url)
        self.assertIn("resourceName=testqueue", url)
        logger.info("Queue SAS token test passed")


def main():
    """Main function to run the tests."""
    logger.info("Starting SAS token generator tests...")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    logger.info("All tests completed")
    
if __name__ == '__main__':
    main() 