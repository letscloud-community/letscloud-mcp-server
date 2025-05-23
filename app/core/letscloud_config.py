from typing import Optional
from pydantic import BaseModel, Field
import os

class LetsCloudConfig(BaseModel):
    """Configuration for LetsCloud SDK integration"""
    api_token: str = Field(
        default_factory=lambda: os.getenv("LETSCLOUD_API_TOKEN", ""),
        description="API token for LetsCloud authentication"
    )
    api_url: str = Field(
        default="https://api.letscloud.io",
        description="LetsCloud API URL"
    )
    timeout: int = Field(
        default=30,
        description="Timeout for API requests in seconds"
    )
    max_retries: int = Field(
        default=3,
        description="Maximum number of retries for failed requests"
    )
    retry_delay: int = Field(
        default=1,
        description="Delay between retries in seconds"
    )

    class Config:
        env_prefix = "LETSCLOUD_" 