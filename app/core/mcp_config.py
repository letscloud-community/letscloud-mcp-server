"""
Configuração centralizada do MCP Server da LetsCloud.

Este módulo define as configurações padrão e constantes para o MCP Server,
garantindo consistência em todas as integrações.
"""

import os
from typing import Dict, Any, List
from pydantic import BaseSettings, Field

class MCPConfig(BaseSettings):
    """Configurações do MCP Server."""
    
    # URL base do MCP Server
    SERVER_URL: str = Field(
        default="https://mcp.letscloud.io",
        description="URL base do MCP Server"
    )
    
    # Configurações de autenticação
    MCP_API_TOKEN: str = Field(
        default=os.getenv("MCP_API_TOKEN", ""),
        description="Token de API do MCP Server para autenticação das IAs"
    )
    
    # Token da API da LetsCloud
    LETSCLOUD_API_TOKEN: str = Field(
        default=os.getenv("LETSCLOUD_API_TOKEN", ""),
        description="Token de API da LetsCloud para operações de infraestrutura"
    )
    
    # Configurações de timeout
    TIMEOUT: int = Field(
        default=30,
        description="Timeout em segundos para requisições"
    )
    
    # Configurações de retry
    MAX_RETRIES: int = Field(
        default=3,
        description="Número máximo de tentativas"
    )
    
    # Configurações de rate limiting
    RATE_LIMIT: int = Field(
        default=100,
        description="Limite de requisições por minuto"
    )
    
    # Ações permitidas
    ALLOWED_ACTIONS: List[str] = Field(
        default=["CREATE", "READ", "UPDATE", "DELETE"],
        description="Ações permitidas no MCP Server"
    )
    
    # Tipos de contexto permitidos
    ALLOWED_CONTEXT_TYPES: List[str] = Field(
        default=[
            "SYSTEM",
            "INFRASTRUCTURE",
            "DATA",
            "ANALYSIS",
            "DECISION",
            "FEEDBACK",
            "ERROR"
        ],
        description="Tipos de contexto permitidos"
    )
    
    # Configurações de logging
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Nível de logging"
    )
    
    # Configurações de segurança
    JWT_SECRET: str = Field(
        default=os.getenv("JWT_SECRET", ""),
        description="Secret para JWT"
    )
    
    # Configurações de cache
    CACHE_TTL: int = Field(
        default=300,
        description="TTL do cache em segundos"
    )
    
    class Config:
        env_prefix = "MCP_"
        case_sensitive = True

# Instância global de configuração
mcp_config = MCPConfig()

def get_client_config(ai_type: str, model: str) -> Dict[str, Any]:
    """
    Retorna configuração padrão para um cliente específico.
    
    Args:
        ai_type: Tipo de IA (chatgpt, claude, gemini)
        model: Modelo específico da IA
        
    Returns:
        Dict com configurações do cliente
    """
    return {
        "server_url": mcp_config.SERVER_URL,
        "mcp_api_token": mcp_config.MCP_API_TOKEN,  # Token para autenticação no MCP Server
        "letscloud_api_token": mcp_config.LETSCLOUD_API_TOKEN,  # Token para operações LetsCloud
        "ai_type": ai_type,
        "model": model,
        "allowed_actions": mcp_config.ALLOWED_ACTIONS,
        "default_metadata": {
            "source": ai_type,
            "environment": "production"
        },
        "timeout": mcp_config.TIMEOUT,
        "max_retries": mcp_config.MAX_RETRIES,
        "rate_limit": mcp_config.RATE_LIMIT
    } 