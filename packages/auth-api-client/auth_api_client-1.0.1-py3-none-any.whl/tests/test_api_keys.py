"""
Tests for the API key management module.
"""

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
import os

# Set fallback mode for testing
os.environ["DB_FALLBACK"] = "true"

from auth.api_keys.example import app
from auth.api_keys.services.api_key_service import APIKeyService
from auth.api_keys.services.token_service import TokenService

# Test client
client = TestClient(app)

@pytest_asyncio.fixture
async def api_key_service():
    """API key service fixture."""
    service = APIKeyService()
    await service.init()
    return service

@pytest_asyncio.fixture
async def test_api_key(api_key_service):
    """Create a test API key."""
    token_data, raw_token = await api_key_service.create_api_key(
        provider_id="test_provider",
        name="test_key",
        environment="test",
        scopes=["api:access"],
        description="Test API key",
        expires_in_days=1
    )
    return raw_token, token_data

def test_public_endpoint():
    """Test public endpoint."""
    response = client.get("/public")
    assert response.status_code == 200
    assert response.json() == {"message": "Public endpoint"}

def test_protected_endpoint_no_key():
    """Test protected endpoint without API key."""
    response = client.get("/protected")
    assert response.status_code == 401
    assert "API key is required" in response.json()["detail"]

@pytest.mark.asyncio
async def test_generate_key(api_key_service):
    """Test API key generation."""
    token_data, raw_token = await api_key_service.create_api_key(
        provider_id="test_provider",
        name="test_key",
        environment="test",
        scopes=["api:access"],
        description="Test API key",
        expires_in_days=1
    )
    
    assert raw_token.startswith("permas_test_")
    assert len(raw_token) > 20
    assert token_data["provider_id"] == "test_provider"
    assert token_data["name"] == "test_key"
    assert token_data["environment"] == "test"
    assert token_data["scopes"] == ["api:access"]
    assert token_data["description"] == "Test API key"
    assert token_data["is_revoked"] is False

@pytest.mark.asyncio
async def test_list_keys(api_key_service, test_api_key):
    """Test API key listing."""
    raw_token, token_data = test_api_key
    
    keys = await api_key_service.list_api_keys("test_provider")
    assert len(keys) >= 1
    
    # Find our test key
    test_key = next((k for k in keys if k["id"] == token_data["id"]), None)
    assert test_key is not None
    assert test_key["provider_id"] == "test_provider"
    assert test_key["name"] == "test_key"

@pytest.mark.asyncio
async def test_revoke_key(api_key_service, test_api_key):
    """Test API key revocation."""
    raw_token, token_data = test_api_key
    
    # Revoke the key
    revoked = await api_key_service.revoke_api_key(token_data["id"], "Testing revocation")
    
    assert revoked["is_revoked"] is True
    assert revoked["revocation_reason"] == "Testing revocation"
    assert revoked["status"] == "revoked"

@pytest.mark.asyncio
async def test_key_usage(api_key_service, test_api_key):
    """Test API key usage tracking."""
    raw_token, token_data = test_api_key
    
    # Log some usage
    await api_key_service.token_service.log_token_usage(
        token_data["id"],
        "/test/endpoint",
        200
    )
    
    # Get usage
    usage = await api_key_service.get_api_key_usage(token_data["id"])
    
    assert usage["request_count"] == 1
    assert "/test/endpoint" in usage["endpoints"]
    assert usage["endpoints"]["/test/endpoint"] == 1
    assert "200" in usage["status_codes"]
    assert usage["status_codes"]["200"] == 1 