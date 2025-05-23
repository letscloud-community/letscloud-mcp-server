"""
Tests for the LetsCloud MCP API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.core.letscloud_client import LetsCloudClient

def test_health_check(client: TestClient):
    """
    Test the health check endpoint.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint(client: TestClient):
    """
    Test the root endpoint.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to LetsCloud MCP API"}

def test_list_servers(client: TestClient, mock_letscloud_client: LetsCloudClient):
    """
    Test the list servers endpoint.
    """
    # Mock the response from LetsCloud client
    mock_servers = [
        {
            "id": 1,
            "name": "Test Server",
            "status": "running",
            "ip": "192.168.1.1"
        }
    ]
    mock_letscloud_client.list_servers.return_value = mock_servers

    # Inject the mock into the app state
    from app.main import app
    app.state.letscloud_client = mock_letscloud_client

    # Make the request
    response = client.get("/api/v1/servers")

    # Assert the response
    assert response.status_code == 200
    assert response.json() == mock_servers

    # Verify the mock was called
    mock_letscloud_client.list_servers.assert_called_once() 