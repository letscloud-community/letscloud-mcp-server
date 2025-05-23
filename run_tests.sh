#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install or update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create temporary .env file for tests
echo "Creating temporary .env file for tests..."
cat > .env << EOL
# Server settings
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=true

# Security settings
JWT_SECRET=test_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database settings
DATABASE_URL=sqlite:///./test.db

# Redis settings
REDIS_URL=redis://localhost:6379/1

# LetsCloud settings
LETSCLOUD_API_TOKEN=test_token
EOL

# Run tests
echo "Running tests..."
pytest

# Remove temporary .env file
rm .env

# Deactivate virtual environment
deactivate 