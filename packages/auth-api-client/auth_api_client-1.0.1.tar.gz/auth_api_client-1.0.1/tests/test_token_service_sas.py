#!/usr/bin/env python3
"""
Integration Tests for Token Service with SAS Authentication
----------------------------------------------------------
This module provides integration tests for the Token Service
using SAS token authentication with Azure Table Storage.
"""

import os
import sys
import unittest
from unittest import mock
import json
import asyncio
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from api_keys.services.token_service import TokenService
from api_keys.services.table_storage import TableStorageClient
from api_keys.services.sas_token_generator import SasTokenGenerator

class TestTokenServiceWithSAS(unittest.TestCase):
    """Test cases for Token Service using SAS authentication."""
    
    def setUp(self):
        """Set up test environment."""
        # Mock environment variables for testing
        self.env_patcher = mock.patch.dict(os.environ, {
            "USE_AZURE_TABLE_STORAGE": "true",
            "USE_AZURE_SAS_GENERATOR": "true",
            "AZURE_STORAGE_ACCOUNT": "teststorageaccount",
            "AZURE_STORAGE_ENDPOINT": "https://teststorageaccount.table.core.windows.net",
            "AZURE_STORAGE_KEY": "test_key_value_1234567890==",
            "AZURE_STORAGE_CONNECTION_STRING": "DefaultEndpointsProtocol=https;AccountName=teststorageaccount;AccountKey=test_key_value_1234567890==;EndpointSuffix=core.windows.net",
            "DB_FALLBACK": "true"  # Enable fallback mode for testing
        })
        self.env_patcher.start()
        
        # Mock the SAS token generator
        self.generator_patcher = mock.patch('api_keys.services.sas_token_generator.SasTokenGenerator')
        self.mock_generator_class = self.generator_patcher.start()
        self.mock_generator = self.mock_generator_class.return_value
        self.mock_generator.generate_table_sas.return_value = "sv=2020-10-02&ss=t&srt=o&sp=rwdlacu&se=2023-06-30T05:11:22Z&sig=MockSASToken"
        self.mock_generator.get_account_endpoint.return_value = "https://teststorageaccount.table.core.windows.net"
        
        # Mock the TableStorageClient
        self.table_client_patcher = mock.patch('api_keys.services.table_storage.TableStorageClient')
        self.mock_table_client_class = self.table_client_patcher.start()
        self.mock_table_client = self.mock_table_client_class.return_value
        self.mock_table_client.initialize.return_value = True
        
        # Mock table operations to simulate successful operations
        self.mock_table_client.create_entity.return_value = True
        self.mock_table_client.update_entity.return_value = True
        self.mock_table_client.get_entity.return_value = {
            "PartitionKey": "provider-1",
            "RowKey": "token-1",
            "id": "token-1",
            "provider_id": "provider-1",
            "name": "Test Token",
            "token_hash": "hash123",
            "scopes": "read,write",
            "status": "active",
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(days=30)).isoformat(),
            "is_revoked": False
        }
        self.mock_table_client.query_entities.return_value = [
            {
                "PartitionKey": "provider-1",
                "RowKey": "token-1",
                "id": "token-1",
                "provider_id": "provider-1",
                "name": "Test Token 1",
                "token_hash": "hash123",
                "scopes": "read,write",
                "status": "active",
                "created_at": datetime.utcnow().isoformat(),
                "expires_at": (datetime.utcnow() + timedelta(days=30)).isoformat(),
                "is_revoked": False
            },
            {
                "PartitionKey": "provider-1",
                "RowKey": "token-2",
                "id": "token-2",
                "provider_id": "provider-1",
                "name": "Test Token 2",
                "token_hash": "hash456",
                "scopes": "read",
                "status": "active",
                "created_at": datetime.utcnow().isoformat(),
                "expires_at": (datetime.utcnow() + timedelta(days=30)).isoformat(),
                "is_revoked": False
            }
        ]
        
        # For SQLite fallback, mock the connection
        self.sqlite_patcher = mock.patch('sqlite3.connect')
        self.mock_sqlite_connect = self.sqlite_patcher.start()
        self.mock_connection = mock.MagicMock()
        self.mock_cursor = mock.MagicMock()
        self.mock_sqlite_connect.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        
        # Create token service instance for tests
        self.token_service = TokenService()
        
        # Mock uuid for consistent test results
        self.uuid_patcher = mock.patch('uuid.uuid4')
        self.mock_uuid = self.uuid_patcher.start()
        self.mock_uuid.return_value = "test-uuid-1234"
    
    def tearDown(self):
        """Clean up after tests."""
        self.env_patcher.stop()
        self.generator_patcher.stop()
        self.table_client_patcher.stop()
        self.sqlite_patcher.stop()
        self.uuid_patcher.stop()
    
    async def test_init_with_sas(self):
        """Test that token service initializes table storage with SAS."""
        # Initialize the token service
        await self.token_service.init()
        
        # Verify that TableStorageClient was initialized
        self.mock_table_client_class.assert_called_once()
        
        # Get the constructor arguments
        args, kwargs = self.mock_table_client_class.call_args
        
        # Verify SAS generator flag was set
        self.assertTrue(kwargs["use_sas_generator"])
        
        # Verify endpoint was passed
        self.assertEqual(kwargs["endpoint"], "https://teststorageaccount.table.core.windows.net")
        
        # Verify the expected tables were included
        self.assertIn("APIKeys", kwargs["table_names"])
        self.assertIn("APIKeyUsage", kwargs["table_names"])
        
        # Verify initialize was called
        self.mock_table_client.initialize.assert_called_once()
    
    async def test_create_token(self):
        """Test creating a token with SAS authentication."""
        # Initialize table client for the test
        self.token_service.table_storage = self.mock_table_client
        self.token_service.use_table_storage = True
        self.token_service._initialized = True
        
        # Create a token
        token_data, raw_token = await self.token_service.create_token(
            provider_id="provider-1",
            name="Test API Key",
            scopes=["read", "write"],
            environment="prod",
            expires_in_days=30,
            description="Test key for SAS auth"
        )
        
        # Verify token was created
        self.assertIsNotNone(token_data)
        self.assertIsNotNone(raw_token)
        self.assertEqual(token_data["provider_id"], "provider-1")
        self.assertEqual(token_data["name"], "Test API Key")
        self.assertEqual(token_data["scopes"], "read,write")
        
        # Verify entity was created in table storage
        self.mock_table_client.create_entity.assert_called()
        
        # Get the entity that was passed to create_entity
        args, kwargs = self.mock_table_client.create_entity.call_args_list[0]
        self.assertEqual(args[0], "APIKeys")  # Table name
        entity = args[1]
        
        # Verify entity has correct data
        self.assertEqual(entity["PartitionKey"], "provider-1")
        self.assertEqual(entity["name"], "Test API Key")
        self.assertEqual(entity["scopes"], "read,write")
        self.assertEqual(entity["environment"], "prod")
    
    async def test_list_tokens(self):
        """Test listing tokens with SAS authentication."""
        # Initialize table client for the test
        self.token_service.table_storage = self.mock_table_client
        self.token_service.use_table_storage = True
        self.token_service._initialized = True
        
        # List tokens for a provider
        tokens = await self.token_service.list_tokens("provider-1")
        
        # Verify tokens were returned
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0]["name"], "Test Token 1")
        self.assertEqual(tokens[1]["name"], "Test Token 2")
        
        # Verify query was made with correct filter
        self.mock_table_client.query_entities.assert_called_once()
        args, kwargs = self.mock_table_client.query_entities.call_args
        self.assertEqual(args[0], "APIKeys")  # Table name
        self.assertEqual(args[1], "PartitionKey eq 'provider-1'")  # Query filter
    
    async def test_validate_token(self):
        """Test token validation with SAS authentication."""
        # Initialize table client for the test
        self.token_service.table_storage = self.mock_table_client
        self.token_service.use_table_storage = True
        self.token_service._initialized = True
        
        # Set up a specific query response for validation
        self.mock_table_client.query_entities.return_value = [{
            "PartitionKey": "provider-1",
            "RowKey": "token-1",
            "id": "token-1",
            "provider_id": "provider-1",
            "name": "Test Token",
            "token_hash": "valid-hash-123",
            "scopes": "read,write",
            "status": "active",
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(days=30)).isoformat(),
            "is_revoked": False,
            "environment": "prod",
            "ip_restrictions": ""
        }]
        
        # Validate a token
        validation = await self.token_service.validate_token("valid-hash-123")
        
        # Verify validation result
        self.assertTrue(validation["valid"])
        self.assertEqual(validation["provider_id"], "provider-1")
        self.assertEqual(validation["scopes"], ["read", "write"])
        self.assertEqual(validation["environment"], "prod")
        
        # Verify query was made with correct filter
        self.mock_table_client.query_entities.assert_called_once()
        args, kwargs = self.mock_table_client.query_entities.call_args
        self.assertEqual(args[0], "APIKeys")  # Table name
        self.assertEqual(args[1], "token_hash eq 'valid-hash-123' and is_revoked eq false")  # Query filter
    
    async def test_log_token_usage(self):
        """Test logging token usage with SAS authentication."""
        # Initialize table client for the test
        self.token_service.table_storage = self.mock_table_client
        self.token_service.use_table_storage = True
        self.token_service._initialized = True
        
        # First test with existing usage record
        usage_entity = {
            "PartitionKey": "token-1",
            "RowKey": "token-1",
            "token_id": "token-1",
            "request_count": 5,
            "last_used": datetime.utcnow().isoformat(),
            "endpoints": json.dumps({"/api/data": 5}),
            "status_codes": json.dumps({"200": 5}),
            "errors": json.dumps([])
        }
        self.mock_table_client.get_entity.return_value = usage_entity
        
        # Log token usage
        await self.token_service.log_token_usage(
            token_id="token-1",
            endpoint="/api/data",
            status_code=200
        )
        
        # Verify update was called
        self.mock_table_client.update_entity.assert_called_once()
        
        # Get the entity that was passed to update_entity
        args, kwargs = self.mock_table_client.update_entity.call_args
        self.assertEqual(args[0], "APIKeyUsage")  # Table name
        updated_entity = args[1]
        
        # Verify entity has correct data
        self.assertEqual(updated_entity["PartitionKey"], "token-1")
        self.assertEqual(updated_entity["RowKey"], "token-1")
        self.assertEqual(updated_entity["request_count"], 6)  # Incremented
        
        # Reset mocks for second test
        self.mock_table_client.reset_mock()
        self.mock_table_client.get_entity.return_value = None
        
        # Test with new usage record
        await self.token_service.log_token_usage(
            token_id="token-2",
            endpoint="/api/users",
            status_code=201,
            error="Test error"
        )
        
        # Verify create was called for new record
        self.mock_table_client.create_entity.assert_called_once()
        
        # Get the entity that was passed to create_entity
        args, kwargs = self.mock_table_client.create_entity.call_args
        self.assertEqual(args[0], "APIKeyUsage")  # Table name
        new_entity = args[1]
        
        # Verify entity has correct data
        self.assertEqual(new_entity["PartitionKey"], "token-2")
        self.assertEqual(new_entity["RowKey"], "token-2")
        self.assertEqual(new_entity["request_count"], 1)
        self.assertIn("/api/users", new_entity["endpoints"])
        self.assertIn("201", new_entity["status_codes"])
        self.assertIn("Test error", new_entity["errors"])
    
    async def test_revoke_token(self):
        """Test revoking a token with SAS authentication."""
        # Initialize table client for the test
        self.token_service.table_storage = self.mock_table_client
        self.token_service.use_table_storage = True
        self.token_service._initialized = True
        
        # Set up query response for finding the token
        self.mock_table_client.query_entities.return_value = [{
            "PartitionKey": "provider-1",
            "RowKey": "token-1",
            "id": "token-1",
            "provider_id": "provider-1",
            "name": "Test Token",
            "is_revoked": False
        }]
        
        # Revoke a token
        revocation = await self.token_service.revoke_token(
            token_id="token-1",
            reason="Security concern"
        )
        
        # Verify revocation result
        self.assertEqual(revocation["id"], "token-1")
        self.assertTrue(revocation["is_revoked"])
        self.assertEqual(revocation["revocation_reason"], "Security concern")
        self.assertEqual(revocation["status"], "revoked")
        
        # Verify update was called with correct entity
        self.mock_table_client.update_entity.assert_called_once()
        args, kwargs = self.mock_table_client.update_entity.call_args
        self.assertEqual(args[0], "APIKeys")  # Table name
        updated_entity = args[1]
        
        # Verify entity has correct data
        self.assertEqual(updated_entity["PartitionKey"], "provider-1")
        self.assertEqual(updated_entity["RowKey"], "token-1")
        self.assertTrue(updated_entity["is_revoked"])
        self.assertEqual(updated_entity["revocation_reason"], "Security concern")
        self.assertEqual(updated_entity["status"], "revoked")


# Run the tests
if __name__ == '__main__':
    # Use asyncio to run async tests
    def run_tests():
        test_loader = unittest.TestLoader()
        test_suite = test_loader.loadTestsFromTestCase(TestTokenServiceWithSAS)
        test_runner = unittest.TextTestRunner()
        test_runner.run(test_suite)
    
    asyncio.run(run_tests()) 