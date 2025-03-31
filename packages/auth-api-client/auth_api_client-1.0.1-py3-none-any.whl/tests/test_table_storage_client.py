#!/usr/bin/env python3
"""
Table Storage Client Test
------------------------
Tests the TableStorageClient module with the hybrid SAS token generation approach.
"""

import os
import sys
import json
import logging
import urllib.request
from unittest import mock
from datetime import datetime

# Modify sys.path to make imports work properly
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

# Mock the auth module structure
import api_keys.services.sas_token_generator as sas_module
import api_keys.services.table_storage as table_module
from api_keys.services.sas_token_generator import SasTokenGenerator
from api_keys.services.table_storage import TableStorageClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("table_storage_test")

def test_table_client_with_sas_generator():
    """Test TableStorageClient with SAS token generator"""
    logger.info("TEST: TableStorageClient with SAS token generator")
    
    # Mock connection string
    connection_string = "DefaultEndpointsProtocol=https;AccountName=teststorageaccount;AccountKey=dGVzdGtleXZhbHVlMTIzNDU2Nzg5MA==;EndpointSuffix=core.windows.net"
    
    # Create client with SAS generator
    client = TableStorageClient(
        connection_string=connection_string,
        use_sas_generator=True
    )
    
    # Mock HTTP response for SAS token generation
    with mock.patch('urllib.request.urlopen') as mock_urlopen:
        # Create mock response
        mock_response = mock.MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = json.dumps({
            "sasToken": "sv=2021-06-08&ss=t&srt=o&sp=raud&se=2023-06-30T05:11:22Z&st=2023-06-29T21:11:22Z&spr=https&sig=MockSig%3D",
            "expiresOn": datetime.utcnow().isoformat()
        }).encode('utf-8')
        
        # Set up the context manager return value
        mock_context = mock.MagicMock()
        mock_context.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_context
        
        # Mock the TableServiceClient to avoid actual Azure calls
        with mock.patch('azure.data.tables.TableServiceClient') as mock_table_service:
            # Mock the client instance
            mock_service_instance = mock.MagicMock()
            mock_table_service.return_value = mock_service_instance
            
            # Mock the from_connection_string method
            mock_table_service.from_connection_string.return_value = mock_service_instance
            
            # Initialize the client
            result = client.initialize()
            
            if result:
                logger.info("✅ TableStorageClient initialization successful")
                
                # Verify SAS token was generated
                if client.sas_token and client.endpoint:
                    logger.info(f"SAS token: {client.sas_token}")
                    logger.info(f"Endpoint: {client.endpoint}")
                    
                    # Verify the table service was created with SAS credentials
                    mock_table_service.assert_called_once()
                    
                    # Verify request was made to generate SAS token
                    mock_urlopen.assert_called_once()
                    return True
                else:
                    logger.error("❌ SAS token or endpoint not set")
                    return False
            else:
                logger.error("❌ TableStorageClient initialization failed")
                return False

def test_table_client_with_sas_fallback():
    """Test TableStorageClient with Function App failure and fallback to direct generation"""
    logger.info("TEST: TableStorageClient with Function App failure and fallback")
    
    # Mock connection string
    connection_string = "DefaultEndpointsProtocol=https;AccountName=teststorageaccount;AccountKey=dGVzdGtleXZhbHVlMTIzNDU2Nzg5MA==;EndpointSuffix=core.windows.net"
    
    # Create client with SAS generator
    client = TableStorageClient(
        connection_string=connection_string,
        use_sas_generator=True
    )
    
    # Mock HTTP request to fail
    with mock.patch('urllib.request.urlopen') as mock_urlopen:
        mock_urlopen.side_effect = Exception("Simulated Function App failure")
        
        # Mock the SasTokenGenerator._generate_table_sas_direct method
        with mock.patch.object(SasTokenGenerator, '_generate_table_sas_direct') as mock_direct:
            # Set up direct generation to succeed
            mock_direct.return_value = "sv=2021-06-08&ss=t&srt=o&sp=raud&se=2023-06-30T05:11:22Z&st=2023-06-29T21:11:22Z&spr=https&sig=DirectSDKMockSig%3D"
            
            # Mock Azure SDK availability
            with mock.patch.object(sas_module, '_AZURE_SDK_AVAILABLE', True):
                
                # Mock the TableServiceClient to avoid actual Azure calls
                with mock.patch('azure.data.tables.TableServiceClient') as mock_table_service:
                    # Mock the client instance
                    mock_service_instance = mock.MagicMock()
                    mock_table_service.return_value = mock_service_instance
                    
                    # Mock the from_connection_string method
                    mock_table_service.from_connection_string.return_value = mock_service_instance
                    
                    # Initialize the client
                    result = client.initialize()
                    
                    if result:
                        logger.info("✅ TableStorageClient initialization with fallback successful")
                        
                        # Verify SAS token was generated via fallback
                        if client.sas_token and client.endpoint:
                            logger.info(f"SAS token: {client.sas_token}")
                            logger.info(f"Endpoint: {client.endpoint}")
                            
                            # Verify the table service was created with SAS credentials
                            mock_table_service.assert_called_once()
                            
                            # Verify both methods were attempted
                            mock_urlopen.assert_called_once()
                            mock_direct.assert_called_once()
                            return True
                        else:
                            logger.error("❌ SAS token or endpoint not set")
                            return False
                    else:
                        logger.error("❌ TableStorageClient initialization with fallback failed")
                        return False

def test_rate_limited_fallback():
    """Test TableStorageClient with rate limiting and fallback"""
    logger.info("TEST: TableStorageClient with rate limiting and fallback")
    
    # Mock connection string
    connection_string = "DefaultEndpointsProtocol=https;AccountName=teststorageaccount;AccountKey=dGVzdGtleXZhbHVlMTIzNDU2Nzg5MA==;EndpointSuffix=core.windows.net"
    
    # Create client with SAS generator
    client = TableStorageClient(
        connection_string=connection_string,
        use_sas_generator=True
    )
    
    # Set up rate limiting to immediately trigger
    client.sas_generator = SasTokenGenerator(
        connection_string=connection_string,
        account_name="teststorageaccount"
    )
    client.sas_generator._rate_limit_max_requests = 0  # Trigger rate limiting immediately
    
    # Mock the SasTokenGenerator._generate_table_sas_direct method for fallback
    with mock.patch.object(SasTokenGenerator, '_generate_table_sas_direct') as mock_direct:
        # Set up direct generation to succeed
        mock_direct.return_value = "sv=2021-06-08&ss=t&srt=o&sp=raud&se=2023-06-30T05:11:22Z&st=2023-06-29T21:11:22Z&spr=https&sig=DirectSDKMockSig%3D"
        
        # Mock Azure SDK availability
        with mock.patch.object(sas_module, '_AZURE_SDK_AVAILABLE', True):
            
            # Mock the TableServiceClient to avoid actual Azure calls
            with mock.patch('azure.data.tables.TableServiceClient') as mock_table_service:
                # Mock the client instance
                mock_service_instance = mock.MagicMock()
                mock_table_service.return_value = mock_service_instance
                
                # Mock the from_connection_string method
                mock_table_service.from_connection_string.return_value = mock_service_instance
                
                # Initialize the client
                result = client.initialize()
                
                if result:
                    logger.info("✅ TableStorageClient initialization with rate limiting successful")
                    
                    # Verify SAS token was generated via fallback
                    if client.sas_token and client.endpoint:
                        logger.info(f"SAS token: {client.sas_token}")
                        logger.info(f"Endpoint: {client.endpoint}")
                        
                        # Verify the table service was created with SAS credentials
                        mock_table_service.assert_called_once()
                        
                        # Verify fallback was used
                        mock_direct.assert_called_once()
                        return True
                    else:
                        logger.error("❌ SAS token or endpoint not set")
                        return False
                else:
                    logger.error("❌ TableStorageClient initialization with rate limiting failed")
                    return False

def main():
    """Run all tests"""
    logger.info("==== TABLE STORAGE CLIENT TESTS ====")
    
    results = []
    
    # Test 1: TableStorageClient with SAS token generator
    results.append(("TableStorageClient with SAS generator", test_table_client_with_sas_generator()))
    
    # Test 2: TableStorageClient with fallback
    results.append(("TableStorageClient with fallback", test_table_client_with_sas_fallback()))
    
    # Test 3: TableStorageClient with rate limiting
    results.append(("TableStorageClient with rate limiting", test_rate_limited_fallback()))
    
    # Print summary
    logger.info("\n==== TEST RESULTS SUMMARY ====")
    success_count = sum(1 for _, success in results if success)
    total_count = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        logger.info(f"{test_name}: {status}")
    
    logger.info(f"Overall: {success_count}/{total_count} tests passed")
    
    # Return success code if all tests passed
    return 0 if success_count == total_count else 1

if __name__ == "__main__":
    sys.exit(main()) 