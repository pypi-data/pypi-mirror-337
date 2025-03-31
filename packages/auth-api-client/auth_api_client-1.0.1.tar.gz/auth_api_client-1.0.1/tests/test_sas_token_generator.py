#!/usr/bin/env python3
"""
Tests for SAS Token Generator and Table Storage Integration
----------------------------------------------------------
This module provides tests for the SAS token generator and its integration
with the Table Storage client.
"""

import os
import sys
import unittest
from unittest import mock
import json
from datetime import datetime
import logging

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from api_keys.services.sas_token_generator import SasTokenGenerator
from api_keys.services.table_storage import TableStorageClient

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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
        self.assertEqual(self.generator.account_name, "teststorageaccount")
        self.assertEqual(self.generator.account_key, "test_key_value_1234567890==")
        self.assertIsNotNone(self.generator.connection_string)
        
    def test_get_account_endpoint(self):
        """Test getting the correct endpoint URL."""
        # Test for each resource type
        table_endpoint = self.generator.get_account_endpoint("table")
        self.assertEqual(table_endpoint, "https://teststorageaccount.table.core.windows.net")
        
        blob_endpoint = self.generator.get_account_endpoint("blob")
        self.assertEqual(blob_endpoint, "https://teststorageaccount.blob.core.windows.net")
        
        queue_endpoint = self.generator.get_account_endpoint("queue")
        self.assertEqual(queue_endpoint, "https://teststorageaccount.queue.core.windows.net")
    
    def test_generate_table_sas(self):
        """Test generating SAS token for table storage."""
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
    
    def test_generate_blob_sas(self):
        """Test generating SAS token for blob storage."""
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
    
    def test_generate_queue_sas(self):
        """Test generating SAS token for queue storage."""
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
        
        # Mock the SAS token generator
        self.generator_patcher = mock.patch('api_keys.services.sas_token_generator.SasTokenGenerator')
        self.mock_generator_class = self.generator_patcher.start()
        self.mock_generator = self.mock_generator_class.return_value
        self.mock_generator.generate_table_sas.return_value = "sv=2020-10-02&ss=t&srt=o&sp=rwdlacu&se=2023-06-30T05:11:22Z&sig=MockSASToken"
        self.mock_generator.get_account_endpoint.return_value = "https://teststorageaccount.table.core.windows.net"
        
        # Mock the Azure Table Storage SDK
        self.table_client_patcher = mock.patch('api_keys.services.table_storage.TableServiceClient')
        self.mock_table_client_class = self.table_client_patcher.start()
        self.mock_table_service = self.mock_table_client_class.return_value
        
        # Mock table client methods
        self.mock_table_client = mock.MagicMock()
        self.mock_table_service.get_table_client.return_value = self.mock_table_client
        
    def tearDown(self):
        """Clean up after tests."""
        self.env_patcher.stop()
        self.generator_patcher.stop()
        self.table_client_patcher.stop()
    
    def test_initialize_with_sas(self):
        """Test initializing TableStorageClient with SAS token."""
        # Test initializing with existing SAS token
        client = TableStorageClient(
            endpoint="https://teststorageaccount.table.core.windows.net",
            sas_token=os.environ["AZURE_STORAGE_SAS_TOKEN"],
            table_names=["TestTable"]
        )
        
        # Initialize the client
        result = client.initialize()
        self.assertTrue(result)
        
        # Verify it used SAS token authentication
        self.mock_table_client_class.assert_called_once()
        args, kwargs = self.mock_table_client_class.call_args
        self.assertEqual(kwargs["endpoint"], "https://teststorageaccount.table.core.windows.net")
        self.assertIsNotNone(kwargs["credential"])
    
    def test_initialize_with_sas_generator(self):
        """Test initializing TableStorageClient with SAS token generator."""
        # Create client with SAS generator
        client = TableStorageClient(
            connection_string=os.environ["AZURE_STORAGE_CONNECTION_STRING"],
            table_names=["TestTable"],
            use_sas_generator=True
        )
        
        # Replace the SasTokenGenerator with our mock
        client.sas_generator = self.mock_generator
        
        # Initialize the client
        result = client.initialize()
        self.assertTrue(result)
        
        # Verify SAS token was generated
        self.mock_generator.generate_table_sas.assert_called_once()
        self.assertEqual(client.sas_token, "sv=2020-10-02&ss=t&srt=o&sp=rwdlacu&se=2023-06-30T05:11:22Z&sig=MockSASToken")
        
        # Verify endpoint was retrieved
        self.mock_generator.get_account_endpoint.assert_called_once()
        self.assertEqual(client.endpoint, "https://teststorageaccount.table.core.windows.net")
        
        # Verify TableServiceClient was created with SAS credentials
        self.mock_table_client_class.assert_called_once()
        args, kwargs = self.mock_table_client_class.call_args
        self.assertEqual(kwargs["endpoint"], "https://teststorageaccount.table.core.windows.net")
        self.assertIsNotNone(kwargs["credential"])
        
    def test_table_operations_with_sas(self):
        """Test that CRUD operations work with SAS token authentication."""
        # Create client with SAS token
        client = TableStorageClient(
            endpoint="https://teststorageaccount.table.core.windows.net",
            sas_token=os.environ["AZURE_STORAGE_SAS_TOKEN"],
            table_names=["TestTable"]
        )
        
        # Initialize and configure mock table client
        client.initialize()
        client.tables["TestTable"] = self.mock_table_client
        
        # Mock the create_entity response
        self.mock_table_client.create_entity.return_value = None
        
        # Test create_entity
        test_entity = {
            "PartitionKey": "test-partition",
            "RowKey": "test-row",
            "Data": "test-data"
        }
        result = client.create_entity("TestTable", test_entity)
        self.assertTrue(result)
        self.mock_table_client.create_entity.assert_called_once_with(entity=test_entity)
        
        # Mock the get_entity response
        self.mock_table_client.get_entity.return_value = test_entity
        
        # Test get_entity
        entity = client.get_entity("TestTable", "test-partition", "test-row")
        self.assertEqual(entity, test_entity)
        self.mock_table_client.get_entity.assert_called_once_with(
            partition_key="test-partition",
            row_key="test-row"
        )


if __name__ == '__main__':
    unittest.main() 