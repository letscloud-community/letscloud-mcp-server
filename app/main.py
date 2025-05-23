"""
Main application module for the LetsCloud MCP API.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.letscloud_client import LetsCloudClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global variable to track application readiness
app_ready = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.
    """
    global app_ready
    try:
        logger.info("Starting up application...")
        # Initialize LetsCloud client
        app.state.letscloud_client = LetsCloudClient(settings.LETSCLOUD_API_TOKEN)
        app_ready = True
        logger.info("Application startup complete")
        yield
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise
    finally:
        logger.info("Shutting down application...")
        app_ready = False
        logger.info("Application shutdown complete")

app = FastAPI(
    title="LetsCloud MCP API",
    description="API for managing LetsCloud servers",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_letscloud_client() -> LetsCloudClient:
    """
    Dependency to get the LetsCloud client.
    """
    return app.state.letscloud_client

@app.get("/")
async def root():
    """
    Root endpoint.
    """
    return {"message": "Welcome to LetsCloud MCP API"}

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    if not app_ready:
        logger.warning("Health check failed: Application not ready")
        raise HTTPException(status_code=503, detail="Application not ready")
    return {"status": "healthy"}

@app.get("/api/v1/servers")
async def list_servers(letscloud_client: LetsCloudClient = Depends(get_letscloud_client)):
    """
    List all servers.
    """
    try:
        return letscloud_client.list_servers()
    except Exception as e:
        logger.error(f"Error listing servers: {str(e)}")
        raise HTTPException(status_code=500, detail="Error listing servers")

@app.get("/api/v1/servers/{server_id}")
async def get_server(server_id: int, letscloud_client: LetsCloudClient = Depends(get_letscloud_client)):
    """
    Get server details.
    """
    try:
        return letscloud_client.get_server(server_id)
    except Exception as e:
        logger.error(f"Error getting server {server_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error getting server details")

@app.post("/api/v1/servers")
async def create_server(server_data: dict, letscloud_client: LetsCloudClient = Depends(get_letscloud_client)):
    """
    Create a new server.
    """
    try:
        return letscloud_client.create_server(server_data)
    except Exception as e:
        logger.error(f"Error creating server: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating server")

@app.delete("/api/v1/servers/{server_id}")
async def delete_server(server_id: int, letscloud_client: LetsCloudClient = Depends(get_letscloud_client)):
    """
    Delete a server.
    """
    try:
        letscloud_client.delete_server(server_id)
        return {"message": "Server deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting server {server_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error deleting server")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    ) 