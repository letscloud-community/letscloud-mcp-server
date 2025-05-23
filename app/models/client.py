from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class Client(BaseModel):
    """Model for MCP client information"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    api_token: str  # Token para autenticação no MCP Server
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    allowed_actions: List[str] = Field(default=["CREATE", "READ", "UPDATE", "DELETE"])
    rate_limit: int = Field(default=100)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 