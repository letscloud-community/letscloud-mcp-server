from enum import Enum
from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class ContextType(str, Enum):
    """Types of context that can be processed by the MCP"""
    SYSTEM = "system"           # System-level operations
    INFRASTRUCTURE = "infrastructure"  # Infrastructure management
    DATA = "data"              # Data operations
    ANALYSIS = "analysis"      # Data analysis
    DECISION = "decision"      # Decision making
    FEEDBACK = "feedback"      # User feedback
    ERROR = "error"            # Error handling

class ContextPriority(str, Enum):
    """Priority levels for context processing"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ContextState(str, Enum):
    """Possible states of a context"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    WAITING = "waiting"

class ContextAction(str, Enum):
    """Possible actions that can be performed"""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    ANALYZE = "analyze"
    DECIDE = "decide"
    RECOMMEND = "recommend"
    VALIDATE = "validate"
    TRANSFORM = "transform"

class Context(BaseModel):
    """Base context model for MCP communication"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: ContextType
    priority: ContextPriority = ContextPriority.MEDIUM
    state: ContextState = ContextState.PENDING
    action: ContextAction
    parameters: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, str] = Field(default_factory=dict)
    parent_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0.0"

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ContextResponse(BaseModel):
    """Response model for context processing"""
    context_id: str
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    next_steps: Optional[List[Dict[str, Any]]] = None
    metadata: Dict[str, str] = Field(default_factory=dict)
    processing_time: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ContextTemplate(BaseModel):
    """Template for creating new contexts"""
    name: str
    description: str
    type: ContextType
    default_parameters: Dict[str, Any] = Field(default_factory=dict)
    required_parameters: List[str] = Field(default_factory=list)
    validation_rules: Dict[str, str] = Field(default_factory=dict)
    example: Dict[str, Any] = Field(default_factory=dict)
    version: str = "1.0.0"

class ContextValidation(BaseModel):
    """Validation rules for context processing"""
    required_parameters: List[str] = Field(default_factory=list)
    parameter_types: Dict[str, str] = Field(default_factory=dict)
    allowed_actions: List[ContextAction] = Field(default_factory=list)
    validation_rules: Dict[str, str] = Field(default_factory=dict)
    custom_validators: Dict[str, str] = Field(default_factory=dict) 