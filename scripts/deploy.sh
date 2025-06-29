#!/bin/bash
# 🚀 LetsCloud MCP Server - Automated Deploy Script (Root Version)
# This script automates the complete server installation on VM as root

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function for logging
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

# Banner
echo -e "${BLUE}"
cat << "EOF"
╔══════════════════════════════════════════════════════════╗
║         LetsCloud MCP Server Deploy (Root)              ║
║            Automated Root Installation Script            ║
╚══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check if running as root
if [[ $EUID -ne 0 ]]; then
    error "❌ This script must be run as root (sudo ./deploy.sh)"
fi

log "🔧 Running deploy as root..."

# Define working directories
WORK_DIR="/opt/letscloud-mcp"
ENV_FILE="$WORK_DIR/.env"
PROJECT_DIR="$WORK_DIR/letscloud-mcp-server"

log "📁 Working directory: $WORK_DIR"

# Create necessary directories
mkdir -p "$WORK_DIR"/{logs,scripts,backups}

# Function to request user input
get_input() {
    local prompt="$1"
    local var_name="$2"
    local default="$3"
    local allow_empty="$4"  # New parameter to allow empty input
    
    if [[ -n "$default" ]]; then
        read -p "$prompt [$default]: " input
        if [[ -z "$input" ]]; then
            input="$default"
        fi
    else
        read -p "$prompt: " input
        # If allow_empty is "true", don't force input
        if [[ "$allow_empty" != "true" ]]; then
            while [[ -z "$input" ]]; do
                read -p "$prompt (required): " input
            done
        fi
    fi
    
    eval "$var_name='$input'"
}

# FORCE configuration if variables are not valid
NEED_CONFIG=false

# Check if we need configuration
if [[ -z "$LETSCLOUD_API_TOKEN" || "$LETSCLOUD_API_TOKEN" == "echo"* ]]; then
    NEED_CONFIG=true
fi

if [[ -z "$MCP_API_KEY" || "$MCP_API_KEY" == "log"* || "$MCP_API_KEY" == "ERROR"* ]]; then
    NEED_CONFIG=true  
fi

if [[ "$NEED_CONFIG" == "true" ]]; then
    log "📋 Configuration required (variables not defined)..."
    echo

    # Clear corrupted variables
    unset LETSCLOUD_API_TOKEN MCP_API_KEY SERVER_PORT DOMAIN

    get_input "🔑 LetsCloud API Token" "LETSCLOUD_API_TOKEN"
    get_input "🔐 HTTP API Key (leave empty to auto-generate)" "MCP_API_KEY" "" "true"
    get_input "🌐 Server Port" "SERVER_PORT" "8000"
    get_input "🏠 Domain (optional, leave empty to use IP)" "DOMAIN" "" "true"

    # Generate API key if not provided
    if [[ -z "$MCP_API_KEY" ]]; then
        MCP_API_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || openssl rand -base64 32)
        log "🔐 API Key auto-generated: $MCP_API_KEY"
    fi
    
    log "✅ Configuration completed!"
    log "🔑 Token: ${LETSCLOUD_API_TOKEN:0:15}..."
    log "🔐 API Key: ${MCP_API_KEY:0:15}..."
else
    log "📋 Using existing valid configurations..."
    log "🔑 Token: ${LETSCLOUD_API_TOKEN:0:15}..."
    log "🔐 API Key: ${MCP_API_KEY:0:15}..."
    log "🌐 Port: $SERVER_PORT"
    log "🏠 Domain: ${DOMAIN:-"(automatic IP)"}"
fi

echo
log "🚀 Starting installation..."

# Update system
log "📦 Updating system..."
apt update && apt upgrade -y

# Install basic dependencies
log "🔧 Installing dependencies..."

# Auto-detect Python version
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '3\.\d+' | head -1)
if [[ -z "$PYTHON_VERSION" ]]; then
    PYTHON_VERSION="3.10"  # Fallback
fi
log "🐍 Python $PYTHON_VERSION detected"

apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    git \
    nginx \
    certbot \
    python3-certbot-nginx \
    htop \
    curl \
    wget \
    unzip \
    ufw \
    fail2ban

# Clone or update repository
if [[ -d "$PROJECT_DIR" ]]; then
    log "🔄 Updating existing repository..."
    git -C "$PROJECT_DIR" pull
else
    log "📥 Cloning repository..."
    git clone https://github.com/letscloud-community/letscloud-mcp-server.git "$PROJECT_DIR"
fi

# Configure Python environment
log "🐍 Configuring Python environment..."
cd "$PROJECT_DIR"

# Create virtual environment
if [[ ! -d "venv" ]]; then
    python3 -m venv venv
fi

# Activate venv and install dependencies
source venv/bin/activate
pip install --upgrade pip

# Install dependencies
if [[ -f "requirements.txt" ]]; then
    pip install -r requirements.txt
else
    # Main dependencies if requirements.txt doesn't exist
    pip install fastapi uvicorn python-dotenv httpx pydantic
fi

# Debug: check variables before saving
# Final validation before saving
if [[ -z "$LETSCLOUD_API_TOKEN" || "$LETSCLOUD_API_TOKEN" == "echo"* ]]; then
    error "❌ LetsCloud API Token is invalid or not defined!"
    exit 1
fi

if [[ -z "$MCP_API_KEY" || "$MCP_API_KEY" == "log"* || "$MCP_API_KEY" == "ERROR"* ]]; then
    error "❌ HTTP API Key is invalid or not defined!"
    exit 1  
fi

log "🔍 Checking configurations before saving:"
log "   Token: ${LETSCLOUD_API_TOKEN:0:15}... (${#LETSCLOUD_API_TOKEN} chars)"
log "   API Key: ${MCP_API_KEY:0:15}... (${#MCP_API_KEY} chars)"
log "   Port: $SERVER_PORT"

log "⚙️ Creating configuration file..."

# Create .env file
cat > "$ENV_FILE" << EOF
LETSCLOUD_API_TOKEN=$LETSCLOUD_API_TOKEN
MCP_API_KEY=$MCP_API_KEY
SERVER_PORT=$SERVER_PORT
DEBUG=false
EOF

log "✅ Configuration file created at $ENV_FILE"

# Configure systemd service
log "🔧 Configuring systemd service..."

# Get public IP
PUBLIC_IP=$(curl -s ifconfig.me || curl -s ipinfo.io/ip || echo "localhost")

cat > /etc/systemd/system/letscloud-mcp.service << EOF
[Unit]
Description=LetsCloud MCP Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$PROJECT_DIR/src
Environment=PATH=$PROJECT_DIR/venv/bin
Environment=PYTHONPATH=$PROJECT_DIR/src
ExecStart=$PROJECT_DIR/venv/bin/python -m uvicorn letscloud_mcp_server.http_server:app --host 0.0.0.0 --port $SERVER_PORT
Restart=always
RestartSec=10
EnvironmentFile=$ENV_FILE

# Security settings
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=$WORK_DIR

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start service
systemctl daemon-reload
systemctl enable letscloud-mcp
systemctl start letscloud-mcp

# Wait for service to start
sleep 3

# Check status
if systemctl is-active --quiet letscloud-mcp; then
    log "✅ Service started successfully!"
else
    warn "⚠️ Service may not have started correctly. Checking logs..."
    journalctl -u letscloud-mcp --no-pager -n 10
fi

# Configure firewall
log "🔥 Configuring firewall..."
ufw --force enable
ufw allow ssh
ufw allow $SERVER_PORT/tcp

# Cleanup
log "🧹 Final cleanup..."
rm -f /tmp/mcp_config.env /tmp/deploy_as_user.sh

# Get final URL
if [[ -n "$DOMAIN" ]]; then
    BASE_URL="http://$DOMAIN:$SERVER_PORT"
else
    BASE_URL="http://$PUBLIC_IP:$SERVER_PORT"
fi

echo
echo -e "${GREEN}"
cat << "EOF"
╔══════════════════════════════════════════════════════════╗
║ ✅ DEPLOY COMPLETED! ║
╚══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

log "📋 Server information:"
echo -e " 🌐 URL: $BASE_URL"
echo -e " 🔑 API Key: $MCP_API_KEY"
echo -e " 📊 Health Check: $BASE_URL/health"
echo -e " 📚 Documentation: $BASE_URL/docs"

echo
log "📋 Useful commands:"
echo -e " Status: systemctl status letscloud-mcp"
echo -e " Logs: journalctl -u letscloud-mcp -f"
echo -e " Restart: systemctl restart letscloud-mcp"

echo
log "🎉 Server ready for use!"

echo
warn "⚠️ Save the API Key: $MCP_API_KEY"
warn "⚠️ Configure your client to use: $BASE_URL"

# Connectivity test
log "🔍 Testing connectivity..."
if curl -f -s "$BASE_URL/health" >/dev/null; then
    log "✅ Health check OK!"
else
    warn "⚠️ Health check failed. Check logs: journalctl -u letscloud-mcp -f"
fi 