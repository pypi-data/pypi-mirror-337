#!/usr/bin/env python3
"""
SAS Token Test Runner
-------------------
Tests the SAS token generation for Azure Table Storage.
This script uses monkeypatching to bypass import issues.
"""

import os
import sys
import logging
import unittest
import unittest.mock as mock
import json
import importlib.util
from datetime import datetime
import builtins

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Store the original __import__ function
original_import = builtins.__import__

# Define a custom import function to handle the api_keys.services imports
def custom_import(name, *args, **kwargs):
    if name == 'api_keys.services.sas_token_generator':
        # Modify the path to directly import the module
        current_dir = os.path.dirname(os.path.abspath(__file__))
        api_keys_dir = os.path.dirname(current_dir)
        module_path = os.path.join(api_keys_dir, 'services', 'sas_token_generator.py')
        
        # Load the module directly
        spec = importlib.util.spec_from_file_location("sas_token_generator", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    else:
        # For all other imports, use the original import function
        return original_import(name, *args, **kwargs)

# Patch the __import__ function
builtins.__import__ = custom_import

# Import our modules directly to avoid issues
current_dir = os.path.dirname(os.path.abspath(__file__))
api_keys_dir = os.path.dirname(current_dir)
sys.path.insert(0, api_keys_dir)

# Now import the modules - this will use our customized import
try:
    from services.sas_token_generator import SasTokenGenerator
    from services.table_storage import TableStorageClient
except Exception as e:
    logger.error(f"Failed to import modules: {str(e)}")
    sys.exit(1)

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

class TestTableStorageWithSAS(unittest.TestCase):
    """Test cases for Table Storage client with SAS token authentication."""
    
    def setUp(self):
        """Set up test environment."""
        # Mock environment variables
        self.env_patcher = mock.patch.dict(os.environ, {
            "AZURE_STORAGE_ACCOUNT": "teststorageaccount",
            "AZURE_STORAGE_ENDPOINT": "https://teststorageaccount.table.core.windows.net",
            "AZURE_STORAGE_KEY": "test_key_value_1234567890==",
            "AZURE_STORAGE_CONNECTION_STRING": "DefaultEndpointsProtocol=https;AccountName=teststorageaccount;AccountKey=test_key_value_1234567890==;EndpointSuffix=core.windows.net",
            "AZURE_STORAGE_SAS_TOKEN": "sv=2020-10-02&ss=t&srt=o&sp=rwdlacu&se=2023-06-30T05:11:22Z&st=2023-06-29T21:11:22Z&spr=https&sig=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmn%3D"
        })
        self.env_patcher.start()
        
        # Mock the table service client
        self.table_client_patcher = mock.patch('azure.data.tables.TableServiceClient')
        self.mock_table_client_class = self.table_client_patcher.start()
        self.mock_table_service = self.mock_table_client_class.return_value
        
        # Mock table client methods
        self.mock_table_client = mock.MagicMock()
        self.mock_table_service.get_table_client.return_value = self.mock_table_client
        
    def tearDown(self):
        """Clean up after tests."""
        self.env_patcher.stop()
        self.table_client_patcher.stop()
    
    def test_initialize_with_sas(self):
        """Test initializing TableStorageClient with SAS token."""
        logger.info("Testing TableStorageClient with SAS token...")
        
        # Create client with SAS token
        client = TableStorageClient(
            endpoint="https://teststorageaccount.table.core.windows.net",
            sas_token=os.environ["AZURE_STORAGE_SAS_TOKEN"],
            table_names=["TestTable"]
        )
        
        # Initialize the client
        result = client.initialize()
        self.assertTrue(result)
        logger.info("Successfully initialized TableStorageClient with SAS token")
        
        # Verify it used SAS token authentication
        self.mock_table_client_class.assert_called_once()
        args, kwargs = self.mock_table_client_class.call_args
        self.assertEqual(kwargs["endpoint"], "https://teststorageaccount.table.core.windows.net")
        self.assertIsNotNone(kwargs["credential"])
        logger.info("SAS token authentication verified")

def run_tests():
    """Run all the tests."""
    logger.info("=== Starting SAS Token and Table Storage Tests ===")
    
    # Create test suites
    sas_suite = unittest.TestLoader().loadTestsFromTestCase(TestSasTokenGenerator)
    table_suite = unittest.TestLoader().loadTestsFromTestCase(TestTableStorageWithSAS)
    
    # Create a test suite combining all test cases
    all_tests = unittest.TestSuite([sas_suite, table_suite])
    
    # Run the tests
    result = unittest.TextTestRunner(verbosity=2).run(all_tests)
    
    # Restore the original import function
    builtins.__import__ = original_import
    
    if result.wasSuccessful():
        logger.info("=== All tests passed successfully ===")
        return 0
    else:
        logger.error("=== Tests failed ===")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests()) 