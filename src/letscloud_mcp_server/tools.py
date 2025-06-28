"""
MCP Tool Definitions
~~~~~~~~~~~~~~~~~~~

Tool definitions for the LetsCloud MCP Server.
Each tool corresponds to a LetsCloud API operation.
"""

from mcp.types import Tool

# Server Management Tools
list_servers_tool = Tool(
    name="list_servers",
    description="List all instances in your LetsCloud account",
    inputSchema={
        "type": "object",
        "properties": {},
        "additionalProperties": False
    }
)

get_server_tool = Tool(
    name="get_server",
    description="Get detailed information about a specific instance",
    inputSchema={
        "type": "object",
        "properties": {
            "server_id": {
                "type": "integer",
                "description": "The ID of the instance to retrieve"
            }
        },
        "required": ["server_id"],
        "additionalProperties": False
    }
)

create_server_tool = Tool(
    name="create_server",
    description="Create a new instance with specified configuration",
    inputSchema={
        "type": "object",
        "properties": {
            "label": {
                "type": "string",
                "description": "A label for the server"
            },
            "plan_slug": {
                "type": "string",
                "description": "The plan slug (e.g., 'basic-1gb', 'standard-2gb')"
            },
            "image_slug": {
                "type": "string",
                "description": "The OS image slug (e.g., 'ubuntu-22-04', 'centos-8')"
            },
            "location_slug": {
                "type": "string",
                "description": "The location slug (e.g., 'nyc1', 'fra1', 'sfo2')"
            },
            "hostname": {
                "type": "string",
                "description": "Custom hostname for the server (optional)"
            },
            "password": {
                "type": "string",
                "description": "Root password for the server (optional, will be auto-generated if not provided)"
            },
            "ssh_keys": {
                "type": "array",
                "items": {
                    "type": "integer"
                },
                "description": "Array of SSH key IDs to add to the server (optional)"
            }
        },
        "required": ["label", "plan_slug", "image_slug", "location_slug"],
        "additionalProperties": False
    }
)

delete_server_tool = Tool(
    name="delete_server",
    description="Delete a server permanently (cannot be undone)",
    inputSchema={
        "type": "object",
        "properties": {
            "server_id": {
                "type": "integer",
                "description": "The ID of the server to delete"
            }
        },
        "required": ["server_id"],
        "additionalProperties": False
    }
)

reboot_server_tool = Tool(
    name="reboot_server",
    description="Reboot a server",
    inputSchema={
        "type": "object",
        "properties": {
            "server_id": {
                "type": "integer",
                "description": "The ID of the server to reboot"
            }
        },
        "required": ["server_id"],
        "additionalProperties": False
    }
)

shutdown_server_tool = Tool(
    name="shutdown_server",
    description="Shutdown a server",
    inputSchema={
        "type": "object",
        "properties": {
            "server_id": {
                "type": "integer",
                "description": "The ID of the server to shutdown"
            }
        },
        "required": ["server_id"],
        "additionalProperties": False
    }
)

start_server_tool = Tool(
    name="start_server",
    description="Start a server that is currently stopped",
    inputSchema={
        "type": "object",
        "properties": {
            "server_id": {
                "type": "integer",
                "description": "The ID of the server to start"
            }
        },
        "required": ["server_id"],
        "additionalProperties": False
    }
)

# SSH Key Management Tools
list_ssh_keys_tool = Tool(
    name="list_ssh_keys",
    description="List all SSH keys in your account",
    inputSchema={
        "type": "object",
        "properties": {},
        "additionalProperties": False
    }
)

get_ssh_key_tool = Tool(
    name="get_ssh_key",
    description="Get detailed information about a specific SSH key",
    inputSchema={
        "type": "object",
        "properties": {
            "key_id": {
                "type": "integer",
                "description": "The ID of the SSH key to retrieve"
            }
        },
        "required": ["key_id"],
        "additionalProperties": False
    }
)

create_ssh_key_tool = Tool(
    name="create_ssh_key",
    description="Add a new SSH key to your account",
    inputSchema={
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "A name for the SSH key"
            },
            "key": {
                "type": "string",
                "description": "The public key content (ssh-rsa, ssh-ed25519, etc.)"
            }
        },
        "required": ["title", "key"],
        "additionalProperties": False
    }
)

delete_ssh_key_tool = Tool(
    name="delete_ssh_key",
    description="Delete an SSH key from your account",
    inputSchema={
        "type": "object",
        "properties": {
            "key_id": {
                "type": "integer",
                "description": "The ID of the SSH key to delete"
            }
        },
        "required": ["key_id"],
        "additionalProperties": False
    }
)

# Snapshot Management Tools
list_snapshots_tool = Tool(
    name="list_snapshots",
    description="List all snapshots for a specific server",
    inputSchema={
        "type": "object",
        "properties": {
            "server_id": {
                "type": "integer",
                "description": "The ID of the server to list snapshots for"
            }
        },
        "required": ["server_id"],
        "additionalProperties": False
    }
)

get_snapshot_tool = Tool(
    name="get_snapshot",
    description="Get detailed information about a specific snapshot",
    inputSchema={
        "type": "object",
        "properties": {
            "server_id": {
                "type": "integer",
                "description": "The ID of the server"
            },
            "snapshot_id": {
                "type": "integer",
                "description": "The ID of the snapshot to retrieve"
            }
        },
        "required": ["server_id", "snapshot_id"],
        "additionalProperties": False
    }
)

create_snapshot_tool = Tool(
    name="create_snapshot",
    description="Create a snapshot of a server",
    inputSchema={
        "type": "object",
        "properties": {
            "server_id": {
                "type": "integer",
                "description": "The ID of the server to snapshot"
            },
            "label": {
                "type": "string",
                "description": "A label for the snapshot"
            },
            "description": {
                "type": "string",
                "description": "A description for the snapshot (optional)"
            }
        },
        "required": ["server_id", "label"],
        "additionalProperties": False
    }
)

delete_snapshot_tool = Tool(
    name="delete_snapshot",
    description="Delete a snapshot permanently",
    inputSchema={
        "type": "object",
        "properties": {
            "server_id": {
                "type": "integer",
                "description": "The ID of the server"
            },
            "snapshot_id": {
                "type": "integer",
                "description": "The ID of the snapshot to delete"
            }
        },
        "required": ["server_id", "snapshot_id"],
        "additionalProperties": False
    }
)

restore_snapshot_tool = Tool(
    name="restore_snapshot",
    description="Restore a server from a snapshot",
    inputSchema={
        "type": "object",
        "properties": {
            "server_id": {
                "type": "integer",
                "description": "The ID of the server to restore"
            },
            "snapshot_id": {
                "type": "integer",
                "description": "The ID of the snapshot to restore from"
            }
        },
        "required": ["server_id", "snapshot_id"],
        "additionalProperties": False
    }
)

# Resource Information Tools
list_plans_tool = Tool(
    name="list_plans",
    description="List all available server plans",
    inputSchema={
        "type": "object",
        "properties": {},
        "additionalProperties": False
    }
)

list_images_tool = Tool(
    name="list_images",
    description="List all available OS images",
    inputSchema={
        "type": "object",
        "properties": {},
        "additionalProperties": False
    }
)

list_locations_tool = Tool(
    name="list_locations",
    description="List all available server locations",
    inputSchema={
        "type": "object",
        "properties": {},
        "additionalProperties": False
    }
)

get_account_info_tool = Tool(
    name="get_account_info",
    description="Get your LetsCloud account information",
    inputSchema={
        "type": "object",
        "properties": {},
        "additionalProperties": False
    }
) 