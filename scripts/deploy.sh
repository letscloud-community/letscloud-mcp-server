#!/bin/bash
# 🚀 LetsCloud MCP Server - Script de Deploy Automatizado
# Este script automatiza a instalação completa do servidor na VM

set -e  # Exit on any error

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log
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

# Verificar se está rodando como root
if [[ $EUID -eq 0 ]]; then
    error "Este script não deve ser executado como root!"
fi

# Verificar se sudo está disponível
if ! command -v sudo &> /dev/null; then
    error "sudo não está instalado. Instale o sudo primeiro."
fi

# Função para solicitar input do usuário
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
            read -p "$prompt (obrigatório): " input
        done
    fi
    
    eval "$var_name='$input'"
}

# Solicitar configurações do usuário
log "📋 Configuração inicial..."
echo

get_input "🔑 Token da API LetsCloud" "LETSCLOUD_API_TOKEN"
get_input "🔐 Chave da API HTTP (deixe vazio para gerar)" "MCP_API_KEY"
get_input "🌐 Porta do servidor" "SERVER_PORT" "8000"
get_input "🏠 Domínio (opcional, deixe vazio para usar IP)" "DOMAIN"

# Gerar chave API se não fornecida
if [[ -z "$MCP_API_KEY" ]]; then
    MCP_API_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || openssl rand -base64 32)
    log "🔐 Chave API gerada automaticamente: $MCP_API_KEY"
fi

echo
log "🚀 Iniciando instalação..."

# Atualizar sistema
log "📦 Atualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar dependências básicas
log "🔧 Instalando dependências..."
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

# Criar usuário mcpserver se não existir
if ! id "mcpserver" &>/dev/null; then
    log "👤 Criando usuário mcpserver..."
    sudo useradd -m -s /bin/bash mcpserver
    sudo usermod -aG sudo mcpserver
else
    log "👤 Usuário mcpserver já existe"
fi

# Configurar diretório home
MCP_HOME="/home/mcpserver"
PROJECT_DIR="$MCP_HOME/letscloud-mcp-server"

# Criar diretórios necessários
sudo -u mcpserver mkdir -p $MCP_HOME/{logs,scripts,backups}

# Clonar ou atualizar repositório
if [[ -d "$PROJECT_DIR" ]]; then
    log "🔄 Atualizando repositório existente..."
    sudo -u mcpserver git -C "$PROJECT_DIR" pull
else
    log "📥 Clonando repositório..."
    sudo -u mcpserver git clone https://github.com/letscloud/letscloud-mcp-server.git "$PROJECT_DIR"
fi

# Configurar ambiente Python
log "🐍 Configurando ambiente Python..."
cd "$PROJECT_DIR"

# Criar ambiente virtual
if [[ ! -d "venv" ]]; then
    sudo -u mcpserver python3.11 -m venv venv
fi

# Ativar venv e instalar dependências
sudo -u mcpserver bash -c "
    source venv/bin/activate
    pip install --upgrade pip
    pip install -e .
"

# Criar arquivo de configuração
log "⚙️ Criando arquivo de configuração..."
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

# Criar script de inicialização
log "📝 Criando script de inicialização..."
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

# Configurar serviço systemd
log "🔄 Configurando serviço systemd..."
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

# Configurar Nginx
log "🌐 Configurando Nginx..."
if [[ -n "$DOMAIN" ]]; then
    SERVER_NAME="$DOMAIN"
else
    # Tentar obter IP público
    SERVER_NAME=$(curl -s ifconfig.me || echo "localhost")
    warn "Usando IP público: $SERVER_NAME"
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

    # Health check (sem autenticação)
    location /health {
        proxy_pass http://127.0.0.1:$SERVER_PORT/health;
        access_log off;
    }
}

# Rate limiting zone
limit_req_zone \$binary_remote_addr zone=api:10m rate=10r/s;
EOF

# Ativar site Nginx
sudo ln -sf /etc/nginx/sites-available/letscloud-mcp /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Testar configuração Nginx
if ! sudo nginx -t; then
    error "Erro na configuração do Nginx"
fi

# Configurar firewall
log "🔒 Configurando firewall..."
sudo ufw --force enable
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'

# Configurar SSL se tiver domínio
if [[ -n "$DOMAIN" && "$DOMAIN" != "localhost" ]]; then
    log "🔐 Configurando SSL para $DOMAIN..."
    
    # Verificar se domínio resolve para este servidor
    if ping -c 1 "$DOMAIN" &>/dev/null; then
        sudo certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos --email "admin@$DOMAIN" || warn "Falha ao configurar SSL"
    else
        warn "Domínio $DOMAIN não resolve para este servidor. Configure o DNS primeiro."
    fi
fi

# Criar script de health check
log "💊 Criando script de health check..."
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

# Adicionar cron job para health check
(sudo -u mcpserver crontab -l 2>/dev/null; echo "*/5 * * * * $MCP_HOME/scripts/health_check.sh >> $MCP_HOME/logs/health.log 2>&1") | sudo -u mcpserver crontab -

# Inicializar serviços
log "🚀 Iniciando serviços..."
sudo systemctl daemon-reload
sudo systemctl enable letscloud-mcp
sudo systemctl restart nginx
sudo systemctl start letscloud-mcp

# Aguardar serviço iniciar
sleep 5

# Verificar status
if sudo systemctl is-active --quiet letscloud-mcp; then
    log "✅ Serviço LetsCloud MCP iniciado com sucesso"
else
    error "❌ Falha ao iniciar serviço LetsCloud MCP"
fi

# Teste final
log "🧪 Testando instalação..."
if curl -s "http://localhost:$SERVER_PORT/health" > /dev/null; then
    log "✅ Health check passou"
else
    warn "❌ Health check falhou"
fi

# Exibir informações finais
echo
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                    ✅ DEPLOY CONCLUÍDO!                  ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo
log "📋 Informações do servidor:"
echo -e "   🌐 URL: http://$SERVER_NAME"
if [[ -n "$DOMAIN" ]]; then
    echo -e "   🔒 HTTPS: https://$DOMAIN (se SSL configurado)"
fi
echo -e "   🔑 API Key: $MCP_API_KEY"
echo -e "   📊 Health Check: http://$SERVER_NAME/health"
echo -e "   📚 Documentação: http://$SERVER_NAME/docs"
echo
log "📋 Comandos úteis:"
echo -e "   Status: sudo systemctl status letscloud-mcp"
echo -e "   Logs: sudo journalctl -u letscloud-mcp -f"
echo -e "   Restart: sudo systemctl restart letscloud-mcp"
echo -e "   Health: $MCP_HOME/scripts/health_check.sh"
echo
log "🎉 Servidor pronto para uso!"
echo
echo -e "${YELLOW}⚠️  Salve a API Key: $MCP_API_KEY${NC}"
echo -e "${YELLOW}⚠️  Configure seu cliente para usar: http://$SERVER_NAME${NC}" 