#!/usr/bin/env python3
"""
Direct SAS Token Integration Test
--------------------------------
Tests the SAS token generation for Azure Table Storage access directly.
This test bypasses the package import structure and imports the modules directly.
"""

import os
import sys
import logging
import unittest
from unittest import mock
import json
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
api_keys_dir = os.path.dirname(current_dir)
auth_dir = os.path.dirname(api_keys_dir)
sys.path.insert(0, auth_dir)

# Direct imports of the modules without going through the package structure
sys.path.insert(0, api_keys_dir)
from services.sas_token_generator import SasTokenGenerator
from services.table_storage import TableStorageClient

# Mock version of Request object for testing
class MockRequest:
    def __init__(self, url):
        self.full_url = url

def test_sas_token_generation():
    """Test generating a SAS token."""
    logger.info("Testing SAS token generation...")
    
    # Mock environment variables
    os.environ["AZURE_STORAGE_ACCOUNT"] = "teststorageaccount"
    os.environ["AZURE_STORAGE_KEY"] = "test_key_value_1234567890=="
    os.environ["AZURE_STORAGE_CONNECTION_STRING"] = "DefaultEndpointsProtocol=https;AccountName=teststorageaccount;AccountKey=test_key_value_1234567890==;EndpointSuffix=core.windows.net"
    
    # Create the SAS token generator
    generator = SasTokenGenerator()
    
    # Mock the HTTP request with Request object
    with mock.patch('urllib.request.urlopen') as mock_urlopen, \
         mock.patch('urllib.request.Request', side_effect=MockRequest) as mock_request:
        # Set up mock response
        mock_response = mock.MagicMock()
        mock_response.status = 200
        mock_response.__enter__.return_value = mock_response
        mock_response.read.return_value = json.dumps({
            "sasToken": "sv=2020-10-02&ss=t&srt=o&sp=raud&se=2023-06-30T05:11:22Z&st=2023-06-29T21:11:22Z&spr=https&sig=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmn%3D",
            "expiresOn": (datetime.utcnow().isoformat() + "Z")
        }).encode('utf-8')
        mock_urlopen.return_value = mock_response
        
        # Create a mock Request to capture the parameters
        url_with_params = "https://func-sas-generator.azurewebsites.net/api/sas?code=xPryOow6elO4bdhKue4J17uz8otUiT4S7w7JE0G5RzPUAzFuJxBqtw==&expiry=24&permissions=raud&resourceType=table&resourceName=TestTable&connectionString=DefaultEndpointsProtocol%3Dhttps%3BAccountName%3Dteststorageaccount%3BAccountKey%3Dtest_key_value_1234567890%3D%3D%3BEndpointSuffix%3Dcore.windows.net"
        mock_request.return_value = MockRequest(url_with_params)
        
        # Get Azure Storage endpoint
        endpoint = generator.get_account_endpoint("table")
        assert endpoint == "https://teststorageaccount.table.core.windows.net"
        logger.info(f"Endpoint URL: {endpoint}")
        
        # Generate SAS token for table storage
        token = generator.generate_table_sas(
            expiry_hours=24,
            permissions="raud",  # Correct order: r=read/query, a=add, u=update, d=delete
            table_name="TestTable"
        )
        
        # Verify token
        assert token is not None
        assert "sv=" in token
        assert "sig=" in token
        logger.info(f"SAS token generated: {token[:20]}...")
        
        # Verify URL parameters
        mock_request.assert_called_once()
        call_args = mock_request.call_args[0]
        url = call_args[0]
        
        assert "resourceType=table" in url
        assert "expiry=24" in url
        assert "permissions=raud" in url
        assert "resourceName=TestTable" in url
        
    return endpoint, token

def test_table_storage_with_sas(endpoint, token):
    """Test initializing TableStorageClient with SAS token."""
    logger.info("Testing TableStorageClient with SAS token...")
    
    # Create TableStorageClient with SAS token
    with mock.patch('services.table_storage.TableServiceClient') as mock_table_client_class:
        mock_table_service = mock_table_client_class.return_value
        mock_table_client = mock.MagicMock()
        mock_table_service.get_table_client.return_value = mock_table_client
        
        client = TableStorageClient(
            endpoint=endpoint,
            sas_token=token,
            table_names=["TestTable"]
        )
        
        # Initialize the client
        result = client.initialize()
        assert result is True
        logger.info("TableStorageClient initialized successfully")
        
        # Verify SAS token authentication was used
        mock_table_client_class.assert_called_once()
        args, kwargs = mock_table_client_class.call_args
        assert kwargs["endpoint"] == endpoint
        assert kwargs["credential"] is not None
        logger.info("SAS token authentication verified")
        
    return True

def test_table_storage_with_generator():
    """Test initializing TableStorageClient with SAS generator."""
    logger.info("Testing TableStorageClient with SAS generator...")
    
    # Mock the SasTokenGenerator
    with mock.patch('services.sas_token_generator.SasTokenGenerator') as mock_generator_class:
        mock_generator = mock_generator_class.return_value
        mock_generator.generate_table_sas.return_value = "sv=2020-10-02&ss=t&srt=o&sp=raud&se=2023-06-30T05:11:22Z&sig=MockSASToken"
        mock_generator.get_account_endpoint.return_value = "https://teststorageaccount.table.core.windows.net"
        
        # Mock the TableServiceClient
        with mock.patch('services.table_storage.TableServiceClient') as mock_table_client_class:
            mock_table_service = mock_table_client_class.return_value
            
            # Create client with SAS generator
            client = TableStorageClient(
                connection_string="DefaultEndpointsProtocol=https;AccountName=teststorageaccount;AccountKey=test_key_value_1234567890==;EndpointSuffix=core.windows.net",
                table_names=["TestTable"],
                use_sas_generator=True
            )
            
            # Replace the SasTokenGenerator with our mock
            client.sas_generator = mock_generator
            
            # Initialize the client
            result = client.initialize()
            assert result is True
            logger.info("TableStorageClient initialized successfully with SAS generator")
            
            # Verify SAS token was generated with proper permissions
            mock_generator.generate_table_sas.assert_called_once_with(
                expiry_hours=24,
                permissions="raud",
                table_name=None
            )
            assert client.sas_token == "sv=2020-10-02&ss=t&srt=o&sp=raud&se=2023-06-30T05:11:22Z&sig=MockSASToken"
            logger.info("SAS token generated correctly")
            
            # Verify endpoint was retrieved
            mock_generator.get_account_endpoint.assert_called_once()
            assert client.endpoint == "https://teststorageaccount.table.core.windows.net"
            logger.info("Endpoint retrieved correctly")
            
    return True

def main():
    """Run the tests."""
    logger.info("=== Starting SAS token generation and Table Storage tests ===")
    
    try:
        # Test SAS token generation
        endpoint, token = test_sas_token_generation()
        if not token:
            logger.error("SAS token generation test failed")
            return 1
        logger.info("✅ SAS token generation test passed")
        
        # Test TableStorageClient with SAS token
        if not test_table_storage_with_sas(endpoint, token):
            logger.error("TableStorageClient with SAS token test failed")
            return 1
        logger.info("✅ TableStorageClient with SAS token test passed")
        
        # Test TableStorageClient with SAS generator
        if not test_table_storage_with_generator():
            logger.error("TableStorageClient with SAS generator test failed")
            return 1
        logger.info("✅ TableStorageClient with SAS generator test passed")
        
        logger.info("=== All tests passed successfully ===")
        return 0
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 