from typing import Dict, Optional
from .protocol import (
    ContextType,
    MCPRequest,
    MCPResponse,
    MCPContext,
    SnapshotContext,
    SSHKeyContext,
    SnapshotState
)
import uuid
from datetime import datetime

class MCPProcessor:
    """Processor for MCP operations."""
    
    def __init__(self):
        self.contexts: Dict[str, MCPContext] = {}

    def process_request(self, request: MCPRequest) -> MCPResponse:
        """Process an MCP request."""
        try:
            if request.context_type == ContextType.SNAPSHOT:
                return self._handle_snapshot_request(request)
            elif request.context_type == ContextType.SSH_KEY:
                return self._handle_ssh_key_request(request)
            else:
                return MCPResponse(
                    success=False,
                    error=f"Unsupported context type: {request.context_type}"
                )
        except Exception as e:
            return MCPResponse(
                success=False,
                error=str(e)
            )

    def _handle_snapshot_request(self, request: MCPRequest) -> MCPResponse:
        """Handle snapshot-related requests."""
        operation = request.operation
        data = request.data

        if operation == "create":
            # Create new snapshot context
            snapshot = SnapshotContext(
                id=str(uuid.uuid4()),
                label=data["label"],
                instance_id=data["instance_id"],
                state=SnapshotState.CREATING
            )
            context = MCPContext(
                type=ContextType.SNAPSHOT,
                data=snapshot.dict()
            )
            self.contexts[snapshot.id] = context
            return MCPResponse(success=True, data=snapshot.dict())

        elif operation == "get":
            # Get snapshot context
            snapshot_id = data["id"]
            if snapshot_id not in self.contexts:
                return MCPResponse(
                    success=False,
                    error=f"Snapshot not found: {snapshot_id}"
                )
            return MCPResponse(
                success=True,
                data=self.contexts[snapshot_id].data
            )

        elif operation == "delete":
            # Delete snapshot context
            snapshot_id = data["id"]
            if snapshot_id not in self.contexts:
                return MCPResponse(
                    success=False,
                    error=f"Snapshot not found: {snapshot_id}"
                )
            snapshot = SnapshotContext(**self.contexts[snapshot_id].data)
            snapshot.state = SnapshotState.DELETING
            self.contexts[snapshot_id].data = snapshot.dict()
            return MCPResponse(success=True)

        else:
            return MCPResponse(
                success=False,
                error=f"Unsupported snapshot operation: {operation}"
            )

    def _handle_ssh_key_request(self, request: MCPRequest) -> MCPResponse:
        """Handle SSH key-related requests."""
        operation = request.operation
        data = request.data

        if operation == "create":
            # Create new SSH key context
            ssh_key = SSHKeyContext(
                id=str(uuid.uuid4()),
                label=data["label"],
                public_key=data["public_key"],
                fingerprint=data["fingerprint"]
            )
            context = MCPContext(
                type=ContextType.SSH_KEY,
                data=ssh_key.dict()
            )
            self.contexts[ssh_key.id] = context
            return MCPResponse(success=True, data=ssh_key.dict())

        elif operation == "get":
            # Get SSH key context
            key_id = data["id"]
            if key_id not in self.contexts:
                return MCPResponse(
                    success=False,
                    error=f"SSH key not found: {key_id}"
                )
            return MCPResponse(
                success=True,
                data=self.contexts[key_id].data
            )

        elif operation == "delete":
            # Delete SSH key context
            key_id = data["id"]
            if key_id not in self.contexts:
                return MCPResponse(
                    success=False,
                    error=f"SSH key not found: {key_id}"
                )
            del self.contexts[key_id]
            return MCPResponse(success=True)

        else:
            return MCPResponse(
                success=False,
                error=f"Unsupported SSH key operation: {operation}"
            ) 