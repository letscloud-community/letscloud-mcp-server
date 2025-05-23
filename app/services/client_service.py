from typing import Optional, List, Dict
import logging
from ..models.client import Client
from ..core.database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class ClientService:
    """Service for managing clients and their tokens"""
    
    def __init__(self, db: Session):
        self.db = db

    def create_client(self, client_data: Dict) -> Client:
        """Create a new client"""
        try:
            client = Client(**client_data)
            self.db.add(client)
            self.db.commit()
            self.db.refresh(client)
            return client
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating client: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))

    def get_client(self, client_id: str) -> Optional[Client]:
        """Get a client by ID"""
        try:
            return self.db.query(Client).filter(Client.id == client_id).first()
        except Exception as e:
            logger.error(f"Error getting client: {str(e)}")
            raise HTTPException(status_code=404, detail="Client not found")

    def get_client_by_token(self, api_token: str) -> Optional[Client]:
        """Get a client by API token"""
        try:
            return self.db.query(Client).filter(Client.api_token == api_token).first()
        except Exception as e:
            logger.error(f"Error getting client by token: {str(e)}")
            raise HTTPException(status_code=404, detail="Client not found")

    def update_client(self, client_id: str, client_data: Dict) -> Client:
        """Update a client"""
        try:
            client = self.get_client(client_id)
            if not client:
                raise HTTPException(status_code=404, detail="Client not found")
            
            for key, value in client_data.items():
                setattr(client, key, value)
            
            self.db.commit()
            self.db.refresh(client)
            return client
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating client: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))

    def delete_client(self, client_id: str) -> None:
        """Delete a client"""
        try:
            client = self.get_client(client_id)
            if not client:
                raise HTTPException(status_code=404, detail="Client not found")
            
            self.db.delete(client)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting client: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))

    def list_clients(self) -> List[Client]:
        """List all clients"""
        try:
            return self.db.query(Client).all()
        except Exception as e:
            logger.error(f"Error listing clients: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e)) 