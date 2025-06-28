#!/bin/bash
# 🚀 LetsCloud MCP Server - Automated Deploy Script
# This script automates the complete server installation on VM

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
║              LetsCloud MCP Server Deploy                ║
║                 Automated Setup Script                  ║
╚══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    warn "⚠️  Detected that you are running as root!"
    echo "For security, it's recommended to run as a non-root user."
    echo
    read -p "🤔 Do you want to automatically create a 'mcpserver' user and continue? (y/n): " create_user
    
    if [[ "$create_user" =~ ^[YySs]$ ]]; then
        log "👤 Creating user 'mcpserver'..."
        
        # Check if user already exists
        if id "mcpserver" &>/dev/null; then
            log "👤 User 'mcpserver' already exists!"
        else
            # Create user
            useradd -m -s /bin/bash mcpserver
            log "✅ User 'mcpserver' created successfully!"
        fi
        
        # Add to sudo group if not already
        usermod -aG sudo mcpserver
        
        # Configure sudo without password for this script
        echo "mcpserver ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/mcpserver-temp
        
        log "🔄 Switching to user 'mcpserver' and continuing..."
        
        # Copy script to /tmp and execute as mcpserver
        cp "$0" /tmp/deploy_as_user.sh 2>/dev/null || {
            # If can't copy current script, download again
            curl -fsSL https://raw.githubusercontent.com/letscloud-community/letscloud-mcp-server/refs/heads/main/scripts/deploy.sh > /tmp/deploy_as_user.sh
        }
        chmod +x /tmp/deploy_as_user.sh
        
        # Execute as mcpserver
        su - mcpserver -c "/tmp/deploy_as_user.sh"
        
        # Clean up temporary sudoers file
        rm -f /etc/sudoers.d/mcpserver-temp
        rm -f /tmp/deploy_as_user.sh
        
        log "🎉 Deploy completed! User 'mcpserver' was created and server is configured."
        exit 0
    else
        echo
        warn "To run manually as non-root user:"
        echo "1. Create user: useradd -m -s /bin/bash mcpserver"
        echo "2. Add to sudo: usermod -aG sudo mcpserver"  
        echo "3. Switch user: su - mcpserver"
        echo "4. Run script: curl -fsSL https://raw.githubusercontent.com/letscloud-community/letscloud-mcp-server/refs/heads/main/scripts/deploy.sh | bash"
        exit 1
    fi
fi

# Check if sudo is available
if ! command -v sudo &> /dev/null; then
    error "sudo is not installed. Please install sudo first."
fi

# Function to request user input
get_input() {
    local prompt="$1"
    local var_name="$2"
    local default="$3"
    
    if [[ -n "$default" ]]; then
        read -p "$prompt [$default]: " input
        if [[ -z "$input" ]]; then
            input="$default"
        fi
    else
        read -p "$prompt: " input
        while [[ -z "$input" ]]; do
            read -p "$prompt (required): " input
        done
    fi
    
    eval "$var_name='$input'"
}

# Request user configurations
log "📋 Initial configuration..."
echo

get_input "🔑 LetsCloud API Token" "LETSCLOUD_API_TOKEN"
get_input "🔐 HTTP API Key (leave empty to auto-generate)" "MCP_API_KEY"
get_input "🌐 Server Port" "SERVER_PORT" "8000"
get_input "🏠 Domain (optional, leave empty to use IP)" "DOMAIN"

# Generate API key if not provided
if [[ -z "$MCP_API_KEY" ]]; then
    MCP_API_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || openssl rand -base64 32)
    log "🔐 API Key auto-generated: $MCP_API_KEY"
fi

echo
log "🚀 Starting installation..."

# Update system
log "📦 Updating system..."
sudo apt update && sudo apt upgrade -y

# Install basic dependencies
log "🔧 Installing dependencies..."
sudo apt install -y \
    python3.11 \
    python3.11-pip \
    python3.11-venv \
    python3.11-dev \
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

# Create mcpserver user if it doesn't exist
if ! id "mcpserver" &>/dev/null; then
    log "👤 Creating mcpserver user..."
    sudo useradd -m -s /bin/bash mcpserver
    sudo usermod -aG sudo mcpserver
else
    log "👤 mcpserver user already exists"
fi

# Configure home directory
MCP_HOME="/home/mcpserver"
PROJECT_DIR="$MCP_HOME/letscloud-mcp-server"

# Create necessary directories
sudo -u mcpserver mkdir -p $MCP_HOME/{logs,scripts,backups}

# Clone or update repository
if [[ -d "$PROJECT_DIR" ]]; then
    log "🔄 Updating existing repository..."
    sudo -u mcpserver git -C "$PROJECT_DIR" pull
else
    log "📥 Cloning repository..."
    sudo -u mcpserver git clone https://github.com/letscloud-community/letscloud-mcp-server.git "$PROJECT_DIR"
fi

# Configure Python environment
log "🐍 Configuring Python environment..."
cd "$PROJECT_DIR"

# Create virtual environment
if [[ ! -d "venv" ]]; then
    sudo -u mcpserver python3.11 -m venv venv
fi

# Activate venv and install dependencies
sudo -u mcpserver bash -c "
    source venv/bin/activate
    pip install --upgrade pip
    pip install -e .
"

# Create configuration file
log "⚙️ Creating configuration file..."
sudo -u mcpserver tee "$MCP_HOME/.env" > /dev/null << EOF
# LetsCloud MCP Server Configuration
LETSCLOUD_API_TOKEN=$LETSCLOUD_API_TOKEN
MCP_API_KEY=$MCP_API_KEY
HOST=0.0.0.0
PORT=$SERVER_PORT
ENVIRONMENT=production
LOG_LEVEL=INFO

# Security
CORS_ORIGINS=*
MAX_CONNECTIONS=100

# Generated on $(date)
EOF

# Create startup script
log "📝 Creating startup script..."
sudo -u mcpserver tee "$MCP_HOME/start_server.py" > /dev/null << 'EOF'
#!/usr/bin/env python3
"""
LetsCloud MCP Server - Production Startup Script
"""
import os
import sys
import asyncio
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent / "letscloud-mcp-server"
sys.path.insert(0, str(project_root / "src"))

try:
    from letscloud_mcp_server.http_server import run_server
    from dotenv import load_dotenv
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all dependencies are installed:")
    print("cd ~/letscloud-mcp-server && source venv/bin/activate && pip install -e .")
    sys.exit(1)

async def main():
    """Start the MCP HTTP server."""
    # Load environment variables
    env_file = Path.home() / ".env"
    if env_file.exists():
        load_dotenv(env_file)
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Starting LetsCloud MCP Server")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Environment: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"   Log Level: {os.getenv('LOG_LEVEL', 'INFO')}")
    
    await run_server(host, port)

if __name__ == "__main__":
    asyncio.run(main())
EOF

sudo chmod +x "$MCP_HOME/start_server.py"

# Configure systemd service
log "🔄 Configuring systemd service..."
sudo tee /etc/systemd/system/letscloud-mcp.service > /dev/null << EOF
[Unit]
Description=LetsCloud MCP Server
After=network.target
Wants=network.target

[Service]
Type=simple
User=mcpserver
Group=mcpserver
WorkingDirectory=$MCP_HOME
Environment=PATH=$PROJECT_DIR/venv/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=$PROJECT_DIR/venv/bin/python $MCP_HOME/start_server.py
Restart=always
RestartSec=10
StartLimitBurst=3
StartLimitInterval=60

# Security
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=$MCP_HOME

# Logs
StandardOutput=journal
StandardError=journal
SyslogIdentifier=letscloud-mcp

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
log "🌐 Configuring Nginx..."
if [[ -n "$DOMAIN" ]]; then
    SERVER_NAME="$DOMAIN"
else
    # Try to get public IP
    SERVER_NAME=$(curl -s ifconfig.me || echo "localhost")
    warn "Using public IP: $SERVER_NAME"
fi

sudo tee /etc/nginx/sites-available/letscloud-mcp > /dev/null << EOF
server {
    listen 80;
    server_name $SERVER_NAME;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self'" always;

    # Rate limiting
    location / {
        limit_req zone=api burst=10 nodelay;
        
        proxy_pass http://127.0.0.1:$SERVER_PORT;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 86400;
        proxy_send_timeout 86400;
    }

    # Health check (no authentication)
    location /health {
        proxy_pass http://127.0.0.1:$SERVER_PORT/health;
        access_log off;
    }
}

# Rate limiting zone
limit_req_zone \$binary_remote_addr zone=api:10m rate=10r/s;
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/letscloud-mcp /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
if ! sudo nginx -t; then
    error "Error in Nginx configuration"
fi

# Configure firewall
log "🔒 Configuring firewall..."
sudo ufw --force enable
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'

# Configure SSL if domain is provided
if [[ -n "$DOMAIN" && "$DOMAIN" != "localhost" ]]; then
    log "🔐 Configuring SSL for $DOMAIN..."
    
    # Check if domain resolves to this server
    if ping -c 1 "$DOMAIN" &>/dev/null; then
        sudo certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos --email "admin@$DOMAIN" || warn "Failed to configure SSL"
    else
        warn "Domain $DOMAIN does not resolve to this server. Configure DNS first."
    fi
fi

# Create health check script
log "💊 Creating health check script..."
sudo -u mcpserver tee "$MCP_HOME/scripts/health_check.sh" > /dev/null << EOF
#!/bin/bash
# Health check script for LetsCloud MCP Server

HEALTH_URL="http://localhost:$SERVER_PORT/health"
RESPONSE=\$(curl -s -o /dev/null -w "%{http_code}" "\$HEALTH_URL" 2>/dev/null)

if [[ "\$RESPONSE" == "200" ]]; then
    echo "✅ LetsCloud MCP Server is healthy"
    exit 0
else
    echo "❌ LetsCloud MCP Server is unhealthy (HTTP \$RESPONSE)"
    
    # Try to restart service
    sudo systemctl restart letscloud-mcp
    sleep 5
    
    # Check again
    RESPONSE=\$(curl -s -o /dev/null -w "%{http_code}" "\$HEALTH_URL" 2>/dev/null)
    if [[ "\$RESPONSE" == "200" ]]; then
        echo "✅ Service restarted successfully"
        exit 0
    else
        echo "❌ Service restart failed"
        exit 1
    fi
fi
EOF

sudo chmod +x "$MCP_HOME/scripts/health_check.sh"

# Add cron job for health check
(sudo -u mcpserver crontab -l 2>/dev/null; echo "*/5 * * * * $MCP_HOME/scripts/health_check.sh >> $MCP_HOME/logs/health.log 2>&1") | sudo -u mcpserver crontab -

# Initialize services
log "🚀 Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable letscloud-mcp
sudo systemctl restart nginx
sudo systemctl start letscloud-mcp

# Wait for service to start
sleep 5

# Check status
if sudo systemctl is-active --quiet letscloud-mcp; then
    log "✅ LetsCloud MCP service started successfully"
else
    error "❌ Failed to start LetsCloud MCP service"
fi

# Final test
log "🧪 Testing installation..."
if curl -s "http://localhost:$SERVER_PORT/health" > /dev/null; then
    log "✅ Health check passed"
else
    warn "❌ Health check failed"
fi

# Display final information
echo
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                    ✅ DEPLOY COMPLETED!                  ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo
log "📋 Server information:"
echo -e "   🌐 URL: http://$SERVER_NAME"
if [[ -n "$DOMAIN" ]]; then
    echo -e "   🔒 HTTPS: https://$DOMAIN (if SSL configured)"
fi
echo -e "   🔑 API Key: $MCP_API_KEY"
echo -e "   📊 Health Check: http://$SERVER_NAME/health"
echo -e "   📚 Documentation: http://$SERVER_NAME/docs"
echo
log "📋 Useful commands:"
echo -e "   Status: sudo systemctl status letscloud-mcp"
echo -e "   Logs: sudo journalctl -u letscloud-mcp -f"
echo -e "   Restart: sudo systemctl restart letscloud-mcp"
echo -e "   Health: $MCP_HOME/scripts/health_check.sh"
echo
log "🎉 Server ready for use!"
echo
echo -e "${YELLOW}⚠️  Save the API Key: $MCP_API_KEY${NC}"
echo -e "${YELLOW}⚠️  Configure your client to use: http://$SERVER_NAME${NC}" 