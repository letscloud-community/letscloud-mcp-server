"""
LetsCloud API Client
~~~~~~~~~~~~~~~~~~~

Async client for LetsCloud API integration with MCP server.
"""

import asyncio
from typing import Any, Dict, List, Optional
import httpx
import logging

logger = logging.getLogger(__name__)

class LetsCloudClient:
    """Async LetsCloud API client."""
    
    def __init__(self, api_token: str, base_url: str = "https://core.letscloud.io/api"):
        """
        Initialize the LetsCloud client.
        
        Args:
            api_token: LetsCloud API token
            base_url: Base URL for the LetsCloud API
        """
        self.api_token = api_token
        self.base_url = base_url
        self.headers = {
            "api-token": api_token,
            "Content-Type": "application/json",
            "User-Agent": "LetsCloud-MCP-Server/1.0.0"
        }
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=30.0,
                headers=self.headers
            )
        return self._client

    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make an async HTTP request to the LetsCloud API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            **kwargs: Additional arguments for the request
            
        Returns:
            API response as dictionary
            
        Raises:
            httpx.HTTPError: If the request fails
        """
        client = await self._get_client()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        logger.info(f"Making {method} request to {url}")
        
        try:
            response = await client.request(method, url, **kwargs)
            response.raise_for_status()
            
            if response.content:
                return response.json()
            return {}
        except httpx.HTTPError as e:
            logger.error(f"HTTP error in {method} {url}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in {method} {url}: {str(e)}")
            raise

    async def close(self):
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

    # Server Management Methods
    async def list_servers(self) -> List[Dict[str, Any]]:
        """
        List all servers.
        
        Returns:
            List of server objects
        """
        response = await self._make_request("GET", "instances")
        return response.get("data", [])

    async def get_server(self, server_id: int) -> Dict[str, Any]:
        """
        Get server details by ID.
        
        Args:
            server_id: Server ID
            
        Returns:
            Server object
        """
        response = await self._make_request("GET", f"instances/{server_id}")
        return response.get("data", {})

    async def create_server(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new server.
        
        Args:
            data: Server creation data containing:
                - label: Server label
                - plan_slug: Plan identifier
                - image_slug: OS image identifier
                - location_slug: Location identifier
                - hostname: (optional) Server hostname
                - password: (optional) Root password
                - ssh_keys: (optional) List of SSH key IDs
                
        Returns:
            Created server object
        """
        response = await self._make_request("POST", "instances", json=data)
        return response.get("data", {})

    async def delete_server(self, server_id: int) -> None:
        """
        Delete a server.
        
        Args:
            server_id: Server ID to delete
        """
        await self._make_request("DELETE", f"instances/{server_id}")

    async def reboot_server(self, server_id: int) -> Dict[str, Any]:
        """
        Reboot a server.
        
        Args:
            server_id: Server ID to reboot
            
        Returns:
            Operation result
        """
        response = await self._make_request("POST", f"instances/{server_id}/reboot")
        return response.get("data", {})

    async def shutdown_server(self, server_id: int) -> Dict[str, Any]:
        """
        Shutdown a server.
        
        Args:
            server_id: Server ID to shutdown
            
        Returns:
            Operation result
        """
        response = await self._make_request("POST", f"instances/{server_id}/shutdown")
        return response.get("data", {})

    async def start_server(self, server_id: int) -> Dict[str, Any]:
        """
        Start a server.
        
        Args:
            server_id: Server ID to start
            
        Returns:
            Operation result
        """
        response = await self._make_request("POST", f"instances/{server_id}/start")
        return response.get("data", {})

    # SSH Key Management Methods
    async def list_ssh_keys(self) -> List[Dict[str, Any]]:
        """
        List all SSH keys.
        
        Returns:
            List of SSH key objects
        """
        response = await self._make_request("GET", "ssh-keys")
        return response.get("data", [])

    async def get_ssh_key(self, key_id: int) -> Dict[str, Any]:
        """
        Get SSH key details by ID.
        
        Args:
            key_id: SSH key ID
            
        Returns:
            SSH key object
        """
        response = await self._make_request("GET", f"ssh-keys/{key_id}")
        return response.get("data", {})

    async def create_ssh_key(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new SSH key.
        
        Args:
            data: SSH key data containing:
                - title: Key title/name
                - key: Public key content
                
        Returns:
            Created SSH key object
        """
        response = await self._make_request("POST", "ssh-keys", json=data)
        return response.get("data", {})

    async def delete_ssh_key(self, key_id: int) -> None:
        """
        Delete an SSH key.
        
        Args:
            key_id: SSH key ID to delete
        """
        await self._make_request("DELETE", f"ssh-keys/{key_id}")

    # Snapshot Management Methods
    async def list_snapshots(self, server_id: int) -> List[Dict[str, Any]]:
        """
        List all snapshots for a server.
        
        Args:
            server_id: Server ID
            
        Returns:
            List of snapshot objects
        """
        response = await self._make_request("GET", f"instances/{server_id}/snapshots")
        return response.get("data", [])

    async def get_snapshot(self, server_id: int, snapshot_id: int) -> Dict[str, Any]:
        """
        Get snapshot details.
        
        Args:
            server_id: Server ID
            snapshot_id: Snapshot ID
            
        Returns:
            Snapshot object
        """
        response = await self._make_request("GET", f"instances/{server_id}/snapshots/{snapshot_id}")
        return response.get("data", {})

    async def create_snapshot(self, server_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a snapshot of a server.
        
        Args:
            server_id: Server ID
            data: Snapshot data containing:
                - label: Snapshot label
                - description: (optional) Snapshot description
                
        Returns:
            Created snapshot object
        """
        response = await self._make_request("POST", f"instances/{server_id}/snapshots", json=data)
        return response.get("data", {})

    async def delete_snapshot(self, server_id: int, snapshot_id: int) -> None:
        """
        Delete a snapshot.
        
        Args:
            server_id: Server ID
            snapshot_id: Snapshot ID to delete
        """
        await self._make_request("DELETE", f"instances/{server_id}/snapshots/{snapshot_id}")

    async def restore_snapshot(self, server_id: int, snapshot_id: int) -> Dict[str, Any]:
        """
        Restore a server from a snapshot.
        
        Args:
            server_id: Server ID
            snapshot_id: Snapshot ID to restore from
            
        Returns:
            Restore operation result
        """
        response = await self._make_request("POST", f"instances/{server_id}/snapshots/{snapshot_id}/restore")
        return response.get("data", {})

    # Resource Information Methods
    async def list_plans(self) -> List[Dict[str, Any]]:
        """
        List available server plans.
        
        Returns:
            List of plan objects
        """
        response = await self._make_request("GET", "plans")
        return response.get("data", [])

    async def list_images(self) -> List[Dict[str, Any]]:
        """
        List available OS images.
        
        Returns:
            List of image objects
        """
        response = await self._make_request("GET", "images")
        return response.get("data", [])

    async def list_locations(self) -> List[Dict[str, Any]]:
        """
        List available server locations.
        
        Returns:
            List of location objects
        """
        response = await self._make_request("GET", "locations")
        return response.get("data", [])

    async def get_account_info(self) -> Dict[str, Any]:
        """
        Get account information.
        
        Returns:
            Account information object
        """
        response = await self._make_request("GET", "profile")
        return response.get("data", {})

    def __del__(self):
        """Cleanup on deletion."""
        if hasattr(self, '_client') and self._client:
            # Try to close the client if it exists
            try:
                asyncio.get_event_loop().create_task(self.close())
            except RuntimeError:
                # Event loop might be closed already
                pass 