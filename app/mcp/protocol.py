from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class ContextType(str, Enum):
    """Enum for MCP context types."""
    SNAPSHOT = "snapshot"
    SSH_KEY = "ssh_key"

class SnapshotState(str, Enum):
    """Enum for snapshot states."""
    CREATING = "creating"
    READY = "ready"
    ERROR = "error"
    DELETING = "deleting"
    DELETED = "deleted"

class SnapshotContext(BaseModel):
    """Context for snapshot operations."""
    id: str = Field(..., description="Unique identifier for the snapshot")
    label: str = Field(..., description="Label for the snapshot")
    instance_id: str = Field(..., description="ID of the instance this snapshot belongs to")
    state: SnapshotState = Field(default=SnapshotState.CREATING, description="Current state of the snapshot")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When the snapshot was created")
    size: Optional[int] = Field(None, description="Size of the snapshot in bytes")
    error: Optional[str] = Field(None, description="Error message if snapshot creation failed")

class SSHKeyContext(BaseModel):
    """Context for SSH key operations."""
    id: str = Field(..., description="Unique identifier for the SSH key")
    label: str = Field(..., description="Label for the SSH key")
    public_key: str = Field(..., description="Public key content")
    fingerprint: str = Field(..., description="Fingerprint of the public key")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When the SSH key was created")
    last_used: Optional[datetime] = Field(None, description="When the SSH key was last used")

class MCPRequest(BaseModel):
    """Base class for MCP requests."""
    context_type: ContextType
    operation: str
    data: Dict

class MCPResponse(BaseModel):
    """Base class for MCP responses."""
    success: bool
    error: Optional[str] = None
    data: Optional[Dict] = None

class MCPContext(BaseModel):
    """Base class for MCP contexts."""
    type: ContextType
    data: Dict 