from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..services.client_service import ClientService
from ..models.client import Client
from ..core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/clients", tags=["Clients"])

def get_client_service(db: Session = Depends(get_db)) -> ClientService:
    return ClientService(db)

@router.post("/", response_model=Client)
async def create_client(
    client_data: dict,
    client_service: ClientService = Depends(get_client_service)
):
    """Create a new client"""
    return client_service.create_client(client_data)

@router.get("/{client_id}", response_model=Client)
async def get_client(
    client_id: str,
    client_service: ClientService = Depends(get_client_service)
):
    """Get a client by ID"""
    return client_service.get_client(client_id)

@router.get("/", response_model=List[Client])
async def list_clients(
    client_service: ClientService = Depends(get_client_service)
):
    """List all clients"""
    return client_service.list_clients()

@router.put("/{client_id}", response_model=Client)
async def update_client(
    client_id: str,
    client_data: dict,
    client_service: ClientService = Depends(get_client_service)
):
    """Update a client"""
    return client_service.update_client(client_id, client_data)

@router.delete("/{client_id}")
async def delete_client(
    client_id: str,
    client_service: ClientService = Depends(get_client_service)
):
    """Delete a client"""
    client_service.delete_client(client_id)
    return {"message": "Client deleted successfully"} 