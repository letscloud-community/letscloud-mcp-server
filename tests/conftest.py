"""
Test fixtures for the LetsCloud MCP API.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.main import app
from app.core.config import settings
from app.core.letscloud_client import LetsCloudClient

@pytest.fixture
def client():
    """
    Test client fixture.
    """
    from app.main import app
    with TestClient(app) as client:
        yield client

@pytest.fixture
def mock_letscloud_client():
    """
    Mock LetsCloud client fixture.
    """
    with patch("app.core.letscloud_client.LetsCloudClient") as mock:
        client = Mock(spec=LetsCloudClient)
        mock.return_value = client
        yield client

@pytest.fixture
def mock_redis():
    """
    Mock Redis client fixture.
    """
    with patch("app.core.redis.Redis") as mock:
        client = Mock()
        mock.return_value = client
        yield client

@pytest.fixture
def mock_db():
    """
    Mock database session fixture.
    """
    with patch("app.db.session.SessionLocal") as mock:
        session = Mock()
        mock.return_value = session
        yield session 