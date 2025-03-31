"""
Integration tests for the API key management endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from auth.api_keys.example import app

client = TestClient(app)

def test_generate_key():
    """Test API key generation endpoint."""
    response = client.post("/auth/keys/generate", json={
        "provider_id": "test_provider",
        "name": "test_key",
        "environment": "test",
        "scopes": ["api:access"],
        "description": "Test API key",
        "expires_in_days": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert "key" in data
    assert "token_info" in data
    assert data["token_info"]["provider_id"] == "test_provider"
    assert data["token_info"]["name"] == "test_key"
    return data["token_info"]["id"]

def test_list_keys():
    """Test API key listing endpoint."""
    response = client.get("/auth/keys?provider_id=test_provider")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "id" in data[0]
        assert "provider_id" in data[0]

def test_revoke_key():
    """Test API key revocation endpoint."""
    # First generate a key
    token_id = test_generate_key()
    
    # Then revoke it
    response = client.post(f"/auth/keys/{token_id}/revoke", json={
        "reason": "Testing revocation"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["is_revoked"] is True
    assert data["revocation_reason"] == "Testing revocation"

def test_get_key_status():
    """Test API key status endpoint."""
    # First generate a key
    token_id = test_generate_key()
    
    # Check initial status
    response = client.get(f"/auth/keys/{token_id}/status")
    assert response.status_code == 200
    data = response.json()
    assert data["is_revoked"] is False
    
    # Revoke the key
    client.post(f"/auth/keys/{token_id}/revoke", json={
        "reason": "Testing status check"
    })
    
    # Check status again
    response = client.get(f"/auth/keys/{token_id}/status")
    assert response.status_code == 200
    data = response.json()
    assert data["is_revoked"] is True

def test_get_key_usage():
    """Test API key usage endpoint."""
    # First generate a key
    token_id = test_generate_key()
    
    # Get usage stats
    response = client.get(f"/auth/keys/{token_id}/usage")
    assert response.status_code == 200
    data = response.json()
    assert "request_count" in data
    assert "endpoints" in data
    assert "status_codes" in data 