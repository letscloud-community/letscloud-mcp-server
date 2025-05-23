from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # MCP Settings
    MCP_API_TOKEN: str
    JWT_SECRET: str
    
    # LetsCloud Settings
    LETSCLOUD_API_URL: str = "https://api.letscloud.io"
    LETSCLOUD_API_VERSION: str = "v1"
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 