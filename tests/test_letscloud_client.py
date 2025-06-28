"""
Tests for LetsCloud API Client
"""

import pytest
import httpx
from unittest.mock import AsyncMock, patch
from src.letscloud_mcp_server.letscloud_client import LetsCloudClient


@pytest.mark.asyncio
class TestLetsCloudClient:
    """Test cases for LetsCloud API client."""

    def setup_method(self):
        """Set up test fixtures."""
        self.api_token = "test-token-123"
        self.client = LetsCloudClient(self.api_token)

    @pytest.fixture
    def mock_response(self):
        """Mock HTTP response."""
        response = AsyncMock()
        response.json.return_value = {"test": "data"}
        response.content = b'{"test": "data"}'
        response.raise_for_status.return_value = None
        return response

    async def test_init(self):
        """Test client initialization."""
        assert self.client.api_token == self.api_token
        assert self.client.base_url == "https://core.letscloud.io/api"
        assert "Bearer test-token-123" in self.client.headers["Authorization"]

    async def test_custom_base_url(self):
        """Test client initialization with custom base URL."""
        custom_url = "https://custom.api.url/v2"
        client = LetsCloudClient(self.api_token, custom_url)
        assert client.base_url == custom_url

    @patch('httpx.AsyncClient.request')
    async def test_make_request_success(self, mock_request, mock_response):
        """Test successful API request."""
        mock_request.return_value = mock_response
        
        result = await self.client._make_request("GET", "test-endpoint")
        
        assert result == {"test": "data"}
        mock_request.assert_called_once()

    @patch('httpx.AsyncClient.request')
    async def test_make_request_http_error(self, mock_request):
        """Test API request with HTTP error."""
        mock_request.side_effect = httpx.HTTPStatusError("404 Not Found", request=None, response=None)
        
        with pytest.raises(httpx.HTTPStatusError):
            await self.client._make_request("GET", "test-endpoint")

    # Server Management Tests
    @patch('src.letscloud_mcp_server.letscloud_client.LetsCloudClient._make_request')
    async def test_list_servers(self, mock_request):
        """Test listing servers."""
        expected_servers = [{"id": 1, "name": "server1"}, {"id": 2, "name": "server2"}]
        mock_request.return_value = expected_servers
        
        result = await self.client.list_servers()
        
        assert result == expected_servers
        mock_request.assert_called_once_with("GET", "instances")

    @patch('src.letscloud_mcp_server.letscloud_client.LetsCloudClient._make_request')
    async def test_get_server(self, mock_request):
        """Test getting server details."""
        server_id = 123
        expected_server = {"id": server_id, "name": "test-server"}
        mock_request.return_value = expected_server
        
        result = await self.client.get_server(server_id)
        
        assert result == expected_server
        mock_request.assert_called_once_with("GET", f"instances/{server_id}")

    @patch('src.letscloud_mcp_server.letscloud_client.LetsCloudClient._make_request')
    async def test_create_server(self, mock_request):
        """Test creating a server."""
        server_data = {
            "label": "test-server",
            "plan_slug": "basic-1gb",
            "image_slug": "ubuntu-22-04",
            "location_slug": "nyc1"
        }
        expected_response = {"id": 123, **server_data}
        mock_request.return_value = expected_response
        
        result = await self.client.create_server(server_data)
        
        assert result == expected_response
        mock_request.assert_called_once_with("POST", "instances", json=server_data)

    @patch('src.letscloud_mcp_server.letscloud_client.LetsCloudClient._make_request')
    async def test_delete_server(self, mock_request):
        """Test deleting a server."""
        server_id = 123
        mock_request.return_value = {}
        
        await self.client.delete_server(server_id)
        
        mock_request.assert_called_once_with("DELETE", f"instances/{server_id}")

    # SSH Key Management Tests  
    @patch('src.letscloud_mcp_server.letscloud_client.LetsCloudClient._make_request')
    async def test_list_ssh_keys(self, mock_request):
        """Test listing SSH keys."""
        expected_keys = [{"id": 1, "title": "key1"}, {"id": 2, "title": "key2"}]
        mock_request.return_value = expected_keys
        
        result = await self.client.list_ssh_keys()
        
        assert result == expected_keys
        mock_request.assert_called_once_with("GET", "ssh-keys")

    @patch('src.letscloud_mcp_server.letscloud_client.LetsCloudClient._make_request')
    async def test_create_ssh_key(self, mock_request):
        """Test creating an SSH key."""
        key_data = {"title": "test-key", "key": "ssh-rsa AAAAB3..."}
        expected_response = {"id": 123, **key_data}
        mock_request.return_value = expected_response
        
        result = await self.client.create_ssh_key(key_data)
        
        assert result == expected_response
        mock_request.assert_called_once_with("POST", "ssh-keys", json=key_data)

    # Snapshot Management Tests
    @patch('src.letscloud_mcp_server.letscloud_client.LetsCloudClient._make_request')
    async def test_list_snapshots(self, mock_request):
        """Test listing snapshots."""
        server_id = 123
        expected_snapshots = [{"id": 1, "label": "snap1"}, {"id": 2, "label": "snap2"}]
        mock_request.return_value = expected_snapshots
        
        result = await self.client.list_snapshots(server_id)
        
        assert result == expected_snapshots
        mock_request.assert_called_once_with("GET", f"instances/{server_id}/snapshots")

    @patch('src.letscloud_mcp_server.letscloud_client.LetsCloudClient._make_request')
    async def test_create_snapshot(self, mock_request):
        """Test creating a snapshot."""
        server_id = 123
        snapshot_data = {"label": "test-snapshot", "description": "Test snapshot"}
        expected_response = {"id": 456, **snapshot_data}
        mock_request.return_value = expected_response
        
        result = await self.client.create_snapshot(server_id, snapshot_data)
        
        assert result == expected_response
        mock_request.assert_called_once_with("POST", f"instances/{server_id}/snapshots", json=snapshot_data)

    # Resource Information Tests
    @patch('src.letscloud_mcp_server.letscloud_client.LetsCloudClient._make_request')
    async def test_list_plans(self, mock_request):
        """Test listing plans."""
        expected_plans = [{"slug": "basic-1gb", "memory": 1024}, {"slug": "standard-2gb", "memory": 2048}]
        mock_request.return_value = expected_plans
        
        result = await self.client.list_plans()
        
        assert result == expected_plans
        mock_request.assert_called_once_with("GET", "plans")

    @patch('src.letscloud_mcp_server.letscloud_client.LetsCloudClient._make_request')
    async def test_list_images(self, mock_request):
        """Test listing images."""
        expected_images = [{"slug": "ubuntu-22-04", "name": "Ubuntu 22.04"}, {"slug": "centos-8", "name": "CentOS 8"}]
        mock_request.return_value = expected_images
        
        result = await self.client.list_images()
        
        assert result == expected_images
        mock_request.assert_called_once_with("GET", "images")

    @patch('src.letscloud_mcp_server.letscloud_client.LetsCloudClient._make_request')
    async def test_list_locations(self, mock_request):
        """Test listing locations."""
        expected_locations = [{"slug": "nyc1", "name": "New York 1"}, {"slug": "fra1", "name": "Frankfurt 1"}]
        mock_request.return_value = expected_locations
        
        result = await self.client.list_locations()
        
        assert result == expected_locations
        mock_request.assert_called_once_with("GET", "locations")

    async def test_client_cleanup(self):
        """Test client cleanup on deletion."""
        # This test ensures the client can be properly cleaned up
        client = LetsCloudClient("test-token")
        await client.close()
        assert client._client is None 