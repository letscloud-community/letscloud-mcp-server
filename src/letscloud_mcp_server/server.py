#!/usr/bin/env python3
"""
LetsCloud MCP Server

A Model Context Protocol server for managing LetsCloud infrastructure.
Provides tools for:
- Server/instance management
- SSH key management  
- Snapshot operations
- Resource monitoring

Usage:
    python -m src.letscloud_mcp_server.server
"""

import asyncio
import json
import os
from typing import Any, Dict, List, Optional
import logging

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.session import ServerSession
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    TextContent,
    Tool,
    EmbeddedResource,
    ErrorCode,
    McpError,
)

from .letscloud_client import LetsCloudClient
from .tools import (
    list_servers_tool,
    get_server_tool,
    create_server_tool,
    delete_server_tool,
    reboot_server_tool,
    shutdown_server_tool,
    start_server_tool,
    list_ssh_keys_tool,
    get_ssh_key_tool,
    create_ssh_key_tool,
    delete_ssh_key_tool,
    create_snapshot_tool,
    get_snapshot_tool,
    list_snapshots_tool,
    delete_snapshot_tool,
    restore_snapshot_tool,
    list_plans_tool,
    list_images_tool,
    list_locations_tool,
    get_account_info_tool,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global server instance
server = Server("letscloud-mcp")

class LetsCloudMCPServer:
    """Main LetsCloud MCP Server class."""
    
    def __init__(self):
        """Initialize the LetsCloud MCP Server."""
        self.letscloud_client: Optional[LetsCloudClient] = None
        self._tools = [
            # Server management tools
            list_servers_tool,
            get_server_tool,
            create_server_tool,
            delete_server_tool,
            reboot_server_tool,
            shutdown_server_tool,
            start_server_tool,
            # SSH key management tools
            list_ssh_keys_tool,
            get_ssh_key_tool,
            create_ssh_key_tool,
            delete_ssh_key_tool,
            # Snapshot management tools
            create_snapshot_tool,
            get_snapshot_tool,
            list_snapshots_tool,
            delete_snapshot_tool,
            restore_snapshot_tool,
            # Resource information tools
            list_plans_tool,
            list_images_tool,
            list_locations_tool,
            get_account_info_tool,
        ]

    def get_letscloud_client(self) -> LetsCloudClient:
        """Get or create LetsCloud client instance."""
        if self.letscloud_client is None:
            api_token = os.getenv("LETSCLOUD_API_TOKEN")
            if not api_token:
                raise McpError(
                    ErrorCode.INVALID_REQUEST,
                    "LETSCLOUD_API_TOKEN environment variable is required"
                )
            self.letscloud_client = LetsCloudClient(api_token)
        return self.letscloud_client

# Create global server instance
mcp_server = LetsCloudMCPServer()

@server.list_tools()
async def list_tools(request: ListToolsRequest) -> ListToolsResult:
    """List available tools."""
    return ListToolsResult(tools=mcp_server._tools)

@server.call_tool()
async def call_tool(request: CallToolRequest) -> CallToolResult:
    """Handle tool calls."""
    try:
        client = mcp_server.get_letscloud_client()
        
        # Route tool calls to appropriate handlers
        # Server management
        if request.name == "list_servers":
            return await _handle_list_servers(client, request.arguments or {})
        elif request.name == "get_server":
            return await _handle_get_server(client, request.arguments or {})
        elif request.name == "create_server":
            return await _handle_create_server(client, request.arguments or {})
        elif request.name == "delete_server":
            return await _handle_delete_server(client, request.arguments or {})
        elif request.name == "reboot_server":
            return await _handle_reboot_server(client, request.arguments or {})
        elif request.name == "shutdown_server":
            return await _handle_shutdown_server(client, request.arguments or {})
        elif request.name == "start_server":
            return await _handle_start_server(client, request.arguments or {})
        # SSH key management
        elif request.name == "list_ssh_keys":
            return await _handle_list_ssh_keys(client, request.arguments or {})
        elif request.name == "get_ssh_key":
            return await _handle_get_ssh_key(client, request.arguments or {})
        elif request.name == "create_ssh_key":
            return await _handle_create_ssh_key(client, request.arguments or {})
        elif request.name == "delete_ssh_key":
            return await _handle_delete_ssh_key(client, request.arguments or {})
        # Snapshot management
        elif request.name == "create_snapshot":
            return await _handle_create_snapshot(client, request.arguments or {})
        elif request.name == "get_snapshot":
            return await _handle_get_snapshot(client, request.arguments or {})
        elif request.name == "list_snapshots":
            return await _handle_list_snapshots(client, request.arguments or {})
        elif request.name == "delete_snapshot":
            return await _handle_delete_snapshot(client, request.arguments or {})
        elif request.name == "restore_snapshot":
            return await _handle_restore_snapshot(client, request.arguments or {})
        # Resource information
        elif request.name == "list_plans":
            return await _handle_list_plans(client, request.arguments or {})
        elif request.name == "list_images":
            return await _handle_list_images(client, request.arguments or {})
        elif request.name == "list_locations":
            return await _handle_list_locations(client, request.arguments or {})
        elif request.name == "get_account_info":
            return await _handle_get_account_info(client, request.arguments or {})
        else:
            raise McpError(
                ErrorCode.METHOD_NOT_FOUND,
                f"Tool '{request.name}' not found"
            )
    except McpError:
        raise
    except Exception as e:
        logger.error(f"Error calling tool {request.name}: {str(e)}")
        raise McpError(
            ErrorCode.INTERNAL_ERROR,
            f"Internal error: {str(e)}"
        )

# Tool handlers
async def _handle_list_servers(client: LetsCloudClient, args: Dict[str, Any]) -> CallToolResult:
    """Handle list servers tool call."""
    try:
        servers = await client.list_servers()
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(servers, indent=2)
                )
            ]
        )
    except Exception as e:
        logger.error(f"Error listing servers: {str(e)}")
        raise McpError(ErrorCode.INTERNAL_ERROR, f"Failed to list servers: {str(e)}")

async def _handle_get_server(client: LetsCloudClient, args: Dict[str, Any]) -> CallToolResult:
    """Handle get server tool call."""
    server_id = args.get("server_id")
    if not server_id:
        raise McpError(ErrorCode.INVALID_PARAMS, "server_id is required")
    
    try:
        server_info = await client.get_server(int(server_id))
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(server_info, indent=2)
                )
            ]
        )
    except Exception as e:
        logger.error(f"Error getting server {server_id}: {str(e)}")
        raise McpError(ErrorCode.INTERNAL_ERROR, f"Failed to get server: {str(e)}")

async def _handle_create_server(client: LetsCloudClient, args: Dict[str, Any]) -> CallToolResult:
    """Handle create server tool call."""
    required_fields = ["label", "plan_slug", "image_slug", "location_slug"]
    for field in required_fields:
        if field not in args:
            raise McpError(ErrorCode.INVALID_PARAMS, f"{field} is required")
    
    try:
        server_info = await client.create_server(args)
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(server_info, indent=2)
                )
            ]
        )
    except Exception as e:
        logger.error(f"Error creating server: {str(e)}")
        raise McpError(ErrorCode.INTERNAL_ERROR, f"Failed to create server: {str(e)}")

async def _handle_delete_server(client: LetsCloudClient, args: Dict[str, Any]) -> CallToolResult:
    """Handle delete server tool call."""
    server_id = args.get("server_id")
    if not server_id:
        raise McpError(ErrorCode.INVALID_PARAMS, "server_id is required")
    
    try:
        await client.delete_server(int(server_id))
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Server {server_id} deleted successfully"
                )
            ]
        )
    except Exception as e:
        logger.error(f"Error deleting server {server_id}: {str(e)}")
        raise McpError(ErrorCode.INTERNAL_ERROR, f"Failed to delete server: {str(e)}")

async def _handle_list_ssh_keys(client: LetsCloudClient, args: Dict[str, Any]) -> CallToolResult:
    """Handle list SSH keys tool call."""
    try:
        ssh_keys = await client.list_ssh_keys()
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(ssh_keys, indent=2)
                )
            ]
        )
    except Exception as e:
        logger.error(f"Error listing SSH keys: {str(e)}")
        raise McpError(ErrorCode.INTERNAL_ERROR, f"Failed to list SSH keys: {str(e)}")

async def _handle_create_ssh_key(client: LetsCloudClient, args: Dict[str, Any]) -> CallToolResult:
    """Handle create SSH key tool call."""
    required_fields = ["title", "key"]
    for field in required_fields:
        if field not in args:
            raise McpError(ErrorCode.INVALID_PARAMS, f"{field} is required")
    
    try:
        ssh_key = await client.create_ssh_key(args)
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(ssh_key, indent=2)
                )
            ]
        )
    except Exception as e:
        logger.error(f"Error creating SSH key: {str(e)}")
        raise McpError(ErrorCode.INTERNAL_ERROR, f"Failed to create SSH key: {str(e)}")

async def _handle_delete_ssh_key(client: LetsCloudClient, args: Dict[str, Any]) -> CallToolResult:
    """Handle delete SSH key tool call."""
    key_id = args.get("key_id")
    if not key_id:
        raise McpError(ErrorCode.INVALID_PARAMS, "key_id is required")
    
    try:
        await client.delete_ssh_key(int(key_id))
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"SSH key {key_id} deleted successfully"
                )
            ]
        )
    except Exception as e:
        logger.error(f"Error deleting SSH key {key_id}: {str(e)}")
        raise McpError(ErrorCode.INTERNAL_ERROR, f"Failed to delete SSH key: {str(e)}")

async def _handle_create_snapshot(client: LetsCloudClient, args: Dict[str, Any]) -> CallToolResult:
    """Handle create snapshot tool call."""
    server_id = args.get("server_id")
    if not server_id:
        raise McpError(ErrorCode.INVALID_PARAMS, "server_id is required")
    
    try:
        snapshot = await client.create_snapshot(int(server_id), args)
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(snapshot, indent=2)
                )
            ]
        )
    except Exception as e:
        logger.error(f"Error creating snapshot: {str(e)}")
        raise McpError(ErrorCode.INTERNAL_ERROR, f"Failed to create snapshot: {str(e)}")

async def _handle_list_snapshots(client: LetsCloudClient, args: Dict[str, Any]) -> CallToolResult:
    """Handle list snapshots tool call."""
    server_id = args.get("server_id")
    if not server_id:
        raise McpError(ErrorCode.INVALID_PARAMS, "server_id is required")
    
    try:
        snapshots = await client.list_snapshots(int(server_id))
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(snapshots, indent=2)
                )
            ]
        )
    except Exception as e:
        logger.error(f"Error listing snapshots: {str(e)}")
        raise McpError(ErrorCode.INTERNAL_ERROR, f"Failed to list snapshots: {str(e)}")

async def _handle_delete_snapshot(client: LetsCloudClient, args: Dict[str, Any]) -> CallToolResult:
    """Handle delete snapshot tool call."""
    server_id = args.get("server_id")
    snapshot_id = args.get("snapshot_id")
    if not server_id or not snapshot_id:
        raise McpError(ErrorCode.INVALID_PARAMS, "server_id and snapshot_id are required")
    
    try:
        await client.delete_snapshot(int(server_id), int(snapshot_id))
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Snapshot {snapshot_id} deleted successfully"
                )
            ]
        )
    except Exception as e:
        logger.error(f"Error deleting snapshot: {str(e)}")
        raise McpError(ErrorCode.INTERNAL_ERROR, f"Failed to delete snapshot: {str(e)}")

async def _handle_restore_snapshot(client: LetsCloudClient, args: Dict[str, Any]) -> CallToolResult:
    """Handle restore snapshot tool call."""
    server_id = args.get("server_id")
    snapshot_id = args.get("snapshot_id")
    if not server_id or not snapshot_id:
        raise McpError(ErrorCode.INVALID_PARAMS, "server_id and snapshot_id are required")
    
    try:
        result = await client.restore_snapshot(int(server_id), int(snapshot_id))
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )
            ]
        )
    except Exception as e:
        logger.error(f"Error restoring snapshot: {str(e)}")
        raise McpError(ErrorCode.INTERNAL_ERROR, f"Failed to restore snapshot: {str(e)}")

# Additional server management handlers
async def _handle_reboot_server(client: LetsCloudClient, args: Dict[str, Any]) -> CallToolResult:
    """Handle reboot server tool call."""
    server_id = args.get("server_id")
    if not server_id:
        raise McpError(ErrorCode.INVALID_PARAMS, "server_id is required")
    
    try:
        result = await client.reboot_server(int(server_id))
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )
            ]
        )
    except Exception as e:
        logger.error(f"Error rebooting server {server_id}: {str(e)}")
        raise McpError(ErrorCode.INTERNAL_ERROR, f"Failed to reboot server: {str(e)}")

async def _handle_shutdown_server(client: LetsCloudClient, args: Dict[str, Any]) -> CallToolResult:
    """Handle shutdown server tool call."""
    server_id = args.get("server_id")
    if not server_id:
        raise McpError(ErrorCode.INVALID_PARAMS, "server_id is required")
    
    try:
        result = await client.shutdown_server(int(server_id))
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )
            ]
        )
    except Exception as e:
        logger.error(f"Error shutting down server {server_id}: {str(e)}")
        raise McpError(ErrorCode.INTERNAL_ERROR, f"Failed to shutdown server: {str(e)}")

async def _handle_start_server(client: LetsCloudClient, args: Dict[str, Any]) -> CallToolResult:
    """Handle start server tool call."""
    server_id = args.get("server_id")
    if not server_id:
        raise McpError(ErrorCode.INVALID_PARAMS, "server_id is required")
    
    try:
        result = await client.start_server(int(server_id))
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )
            ]
        )
    except Exception as e:
        logger.error(f"Error starting server {server_id}: {str(e)}")
        raise McpError(ErrorCode.INTERNAL_ERROR, f"Failed to start server: {str(e)}")

# SSH key management handlers
async def _handle_get_ssh_key(client: LetsCloudClient, args: Dict[str, Any]) -> CallToolResult:
    """Handle get SSH key tool call."""
    key_id = args.get("key_id")
    if not key_id:
        raise McpError(ErrorCode.INVALID_PARAMS, "key_id is required")
    
    try:
        ssh_key = await client.get_ssh_key(int(key_id))
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(ssh_key, indent=2)
                )
            ]
        )
    except Exception as e:
        logger.error(f"Error getting SSH key {key_id}: {str(e)}")
        raise McpError(ErrorCode.INTERNAL_ERROR, f"Failed to get SSH key: {str(e)}")

# Snapshot management handlers
async def _handle_get_snapshot(client: LetsCloudClient, args: Dict[str, Any]) -> CallToolResult:
    """Handle get snapshot tool call."""
    server_id = args.get("server_id")
    snapshot_id = args.get("snapshot_id")
    if not server_id or not snapshot_id:
        raise McpError(ErrorCode.INVALID_PARAMS, "server_id and snapshot_id are required")
    
    try:
        snapshot = await client.get_snapshot(int(server_id), int(snapshot_id))
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(snapshot, indent=2)
                )
            ]
        )
    except Exception as e:
        logger.error(f"Error getting snapshot: {str(e)}")
        raise McpError(ErrorCode.INTERNAL_ERROR, f"Failed to get snapshot: {str(e)}")

# Resource information handlers
async def _handle_list_plans(client: LetsCloudClient, args: Dict[str, Any]) -> CallToolResult:
    """Handle list plans tool call."""
    try:
        plans = await client.list_plans()
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(plans, indent=2)
                )
            ]
        )
    except Exception as e:
        logger.error(f"Error listing plans: {str(e)}")
        raise McpError(ErrorCode.INTERNAL_ERROR, f"Failed to list plans: {str(e)}")

async def _handle_list_images(client: LetsCloudClient, args: Dict[str, Any]) -> CallToolResult:
    """Handle list images tool call."""
    try:
        images = await client.list_images()
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(images, indent=2)
                )
            ]
        )
    except Exception as e:
        logger.error(f"Error listing images: {str(e)}")
        raise McpError(ErrorCode.INTERNAL_ERROR, f"Failed to list images: {str(e)}")

async def _handle_list_locations(client: LetsCloudClient, args: Dict[str, Any]) -> CallToolResult:
    """Handle list locations tool call."""
    try:
        locations = await client.list_locations()
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(locations, indent=2)
                )
            ]
        )
    except Exception as e:
        logger.error(f"Error listing locations: {str(e)}")
        raise McpError(ErrorCode.INTERNAL_ERROR, f"Failed to list locations: {str(e)}")

async def _handle_get_account_info(client: LetsCloudClient, args: Dict[str, Any]) -> CallToolResult:
    """Handle get account info tool call."""
    try:
        account_info = await client.get_account_info()
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(account_info, indent=2)
                )
            ]
        )
    except Exception as e:
        logger.error(f"Error getting account info: {str(e)}")
        raise McpError(ErrorCode.INTERNAL_ERROR, f"Failed to get account info: {str(e)}")

def create_server():
    """Create and return the MCP server instance."""
    return server

async def main():
    """Main entry point for the MCP server."""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="letscloud-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main()) 