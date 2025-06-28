#!/usr/bin/env python3
"""
LetsCloud MCP HTTP Server

HTTP/WebSocket server for remote access to LetsCloud MCP Server.
Provides secure remote access via web endpoints.
"""

import asyncio
import json
import os
import logging
from typing import Any, Dict, Optional
from fastapi import FastAPI, WebSocket, HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from .server import server, mcp_server

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="LetsCloud MCP Server",
    description="Remote access to LetsCloud infrastructure management via MCP",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

def get_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Validate API key for HTTP endpoints."""
    expected_key = os.getenv("MCP_API_KEY")
    if not expected_key:
        raise HTTPException(status_code=500, detail="MCP_API_KEY not configured")
    
    if credentials.credentials != expected_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return credentials.credentials

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "LetsCloud MCP Server",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "websocket": "/mcp",
            "tools": "/tools",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Detailed health check."""
    try:
        # Test LetsCloud client connection
        client = mcp_server.get_letscloud_client()
        # Simple API test (without making actual call)
        return {
            "status": "healthy",
            "mcp_server": "running",
            "letscloud_client": "configured",
            "tools_available": len(mcp_server._tools)
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy", 
                "error": str(e)
            }
        )

@app.get("/tools")
async def list_tools(api_key: str = Depends(get_api_key)):
    """List available MCP tools."""
    try:
        tools = mcp_server._tools
        return {
            "tools": [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema
                }
                for tool in tools
            ],
            "total": len(tools)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/{tool_name}")
async def call_tool(
    tool_name: str,
    request: Dict[str, Any],
    api_key: str = Depends(get_api_key)
):
    """Call a specific MCP tool via HTTP."""
    try:
        result = await server.call_tool(tool_name, request.get("arguments", {}))
        
        return {
            "tool": tool_name,
            "result": {
                "content": [
                    {
                        "type": content.type,
                        "text": content.text
                    }
                    for content in result.content
                ],
                "isError": getattr(result, 'isError', False)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/mcp")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for MCP communication."""
    await websocket.accept()
    logger.info("WebSocket connection established")
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different MCP methods
            if message.get("method") == "initialize":
                response = {
                    "id": message.get("id"),
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {"listChanged": True}
                        },
                        "serverInfo": {
                            "name": "letscloud-mcp",
                            "version": "1.0.0"
                        }
                    }
                }
                await websocket.send_text(json.dumps(response))
                
            elif message.get("method") == "tools/list":
                tools = mcp_server._tools
                response = {
                    "id": message.get("id"),
                    "result": {
                        "tools": [
                            {
                                "name": tool.name,
                                "description": tool.description,
                                "inputSchema": tool.inputSchema
                            }
                            for tool in tools
                        ]
                    }
                }
                await websocket.send_text(json.dumps(response))
                
            elif message.get("method") == "tools/call":
                params = message.get("params", {})
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                try:
                    result = await server.call_tool(tool_name, arguments)
                    response = {
                        "id": message.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": content.type,
                                    "text": content.text
                                }
                                for content in result.content
                            ],
                            "isError": getattr(result, 'isError', False)
                        }
                    }
                    await websocket.send_text(json.dumps(response))
                except Exception as e:
                    error_response = {
                        "id": message.get("id"),
                        "error": {
                            "code": -32603,
                            "message": str(e)
                        }
                    }
                    await websocket.send_text(json.dumps(error_response))
            
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        logger.info("WebSocket connection closed")

def create_app() -> FastAPI:
    """Factory function to create FastAPI app."""
    return app

async def run_server(host: str = "0.0.0.0", port: int = 8000):
    """Run the HTTP server."""
    config = uvicorn.Config(
        app=app,
        host=host,
        port=port,
        log_level="info",
        access_log=True
    )
    server_instance = uvicorn.Server(config)
    await server_instance.serve()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="LetsCloud MCP HTTP Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind")
    
    args = parser.parse_args()
    
    asyncio.run(run_server(args.host, args.port)) 