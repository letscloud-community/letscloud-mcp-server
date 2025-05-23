"""
Configuration settings for the application.
"""

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    Application settings.
    """
    # Server settings
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    DEBUG: bool = False

    # Security settings
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database settings
    DATABASE_URL: str = "sqlite:///./app.db"

    # Redis settings
    REDIS_URL: str = "redis://localhost:6379/0"

    # LetsCloud settings
    LETSCLOUD_API_TOKEN: str

    class Config:
        env_file = ".env"
        case_sensitive = True

# Instância global das configurações
settings = Settings() 