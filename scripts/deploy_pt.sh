#!/bin/bash
# 🚀 LetsCloud MCP Server - Script de Deploy Automatizado (Root Version)
# Este script automatiza a instalação completa do servidor na VM como root

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
║          LetsCloud MCP Server Deploy (Root)             ║
║             Script de Instalação como Root               ║
╚══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Verificar se está rodando como root
if [[ $EUID -ne 0 ]]; then
    error "❌ Este script deve ser executado como root (sudo ./deploy_pt.sh)"
fi

log "🔧 Executando deploy como root..."

# Definir diretórios de trabalho
WORK_DIR="/opt/letscloud-mcp"
ENV_FILE="$WORK_DIR/.env"
PROJECT_DIR="$WORK_DIR/letscloud-mcp-server"

log "📁 Diretório de trabalho: $WORK_DIR"

# Criar diretórios necessários
mkdir -p "$WORK_DIR"/{logs,scripts,backups}

# Função para solicitar input do usuário
get_input() {
    local prompt="$1"
    local var_name="$2"
    local default="$3"
    local allow_empty="$4"  # Novo parâmetro para permitir vazio
    
    if [[ -n "$default" ]]; then
        read -p "$prompt [$default]: " input
        if [[ -z "$input" ]]; then
            input="$default"
        fi
    else
        read -p "$prompt: " input
        # Se allow_empty for "true", não forçar input
        if [[ "$allow_empty" != "true" ]]; then
            while [[ -z "$input" ]]; do
                read -p "$prompt (obrigatório): " input
            done
        fi
    fi
    
    eval "$var_name='$input'"
}

# FORÇA configuração se as variáveis não estão válidas
NEED_CONFIG=false

# Verificar se precisamos de configuração
if [[ -z "$LETSCLOUD_API_TOKEN" || "$LETSCLOUD_API_TOKEN" == "echo"* ]]; then
    NEED_CONFIG=true
fi

if [[ -z "$MCP_API_KEY" || "$MCP_API_KEY" == "log"* || "$MCP_API_KEY" == "ERROR"* ]]; then
    NEED_CONFIG=true  
fi

if [[ "$NEED_CONFIG" == "true" ]]; then
    log "📋 Configuração necessária (variáveis não definidas)..."
    echo

    # Limpar variáveis corrompidas
    unset LETSCLOUD_API_TOKEN MCP_API_KEY SERVER_PORT DOMAIN

    get_input "🔑 Token da API LetsCloud" "LETSCLOUD_API_TOKEN"
    get_input "🔐 Chave da API HTTP (deixe vazio para gerar)" "MCP_API_KEY" "" "true"
    get_input "🌐 Porta do servidor" "SERVER_PORT" "8000"
    get_input "🏠 Domínio (opcional, deixe vazio para usar IP)" "DOMAIN" "" "true"

    # Gerar chave API se não fornecida
    if [[ -z "$MCP_API_KEY" ]]; then
        MCP_API_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || openssl rand -base64 32)
        log "🔐 Chave API gerada automaticamente: $MCP_API_KEY"
    fi
    
    log "✅ Configuração concluída!"
    log "🔑 Token: ${LETSCLOUD_API_TOKEN:0:15}..."
    log "🔐 API Key: ${MCP_API_KEY:0:15}..."
else
    log "📋 Usando configurações válidas existentes..."
    log "🔑 Token: ${LETSCLOUD_API_TOKEN:0:15}..."
    log "🔐 API Key: ${MCP_API_KEY:0:15}..."
    log "🌐 Porta: $SERVER_PORT"
    log "🏠 Domínio: ${DOMAIN:-"(IP automático)"}"
fi

echo
log "🚀 Iniciando instalação..."

# Atualizar sistema
log "📦 Atualizando sistema..."
apt update && apt upgrade -y

# Instalar dependências básicas
log "🔧 Instalando dependências..."

# Auto-detectar versão do Python
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '3\.\d+' | head -1)
if [[ -z "$PYTHON_VERSION" ]]; then
    PYTHON_VERSION="3.10"  # Fallback
fi
log "🐍 Python $PYTHON_VERSION detectado"

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

# Clonar ou atualizar repositório
if [[ -d "$PROJECT_DIR" ]]; then
    log "🔄 Atualizando repositório existente..."
    git -C "$PROJECT_DIR" pull
else
    log "📥 Clonando repositório..."
    git clone https://github.com/letscloud-community/letscloud-mcp-server.git "$PROJECT_DIR"
fi

# Configurar ambiente Python
log "🐍 Configurando ambiente Python..."
cd "$PROJECT_DIR"

# Criar ambiente virtual
if [[ ! -d "venv" ]]; then
    python3 -m venv venv
fi

# Ativar venv e instalar dependências
source venv/bin/activate
pip install --upgrade pip

# Instalar dependências
if [[ -f "requirements.txt" ]]; then
    pip install -r requirements.txt
else
    # Dependências principais se requirements.txt não existir
    pip install fastapi uvicorn python-dotenv httpx pydantic
fi

# Debug: verificar variáveis antes de salvar
# Validação final antes de salvar
if [[ -z "$LETSCLOUD_API_TOKEN" || "$LETSCLOUD_API_TOKEN" == "echo"* ]]; then
    error "❌ Token da API LetsCloud inválido ou não definido!"
    exit 1
fi

if [[ -z "$MCP_API_KEY" || "$MCP_API_KEY" == "log"* || "$MCP_API_KEY" == "ERROR"* ]]; then
    error "❌ Chave API HTTP inválida ou não definida!"
    exit 1  
fi

log "🔍 Verificando configurações antes de salvar:"
log "   Token: ${LETSCLOUD_API_TOKEN:0:15}... (${#LETSCLOUD_API_TOKEN} chars)"
log "   API Key: ${MCP_API_KEY:0:15}... (${#MCP_API_KEY} chars)"
log "   Porta: $SERVER_PORT"

log "⚙️ Criando arquivo de configuração..."

# Criar arquivo .env
cat > "$ENV_FILE" << EOF
LETSCLOUD_API_TOKEN=$LETSCLOUD_API_TOKEN
MCP_API_KEY=$MCP_API_KEY
SERVER_PORT=$SERVER_PORT
DEBUG=false
EOF

log "✅ Arquivo de configuração criado em $ENV_FILE"

# Configurar serviço systemd
log "🔧 Configurando serviço systemd..."

# Obter IP público
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
ExecStart=$PROJECT_DIR/venv/bin/python -m uvicorn letscloud_mcp_server.server:app --host 0.0.0.0 --port $SERVER_PORT
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

# Recarregar systemd e iniciar serviço
systemctl daemon-reload
systemctl enable letscloud-mcp
systemctl start letscloud-mcp

# Aguardar serviço iniciar
sleep 3

# Verificar status
if systemctl is-active --quiet letscloud-mcp; then
    log "✅ Serviço iniciado com sucesso!"
else
    warn "⚠️ Serviço pode não ter iniciado corretamente. Verificando logs..."
    journalctl -u letscloud-mcp --no-pager -n 10
fi

# Configurar firewall
log "🔥 Configurando firewall..."
ufw --force enable
ufw allow ssh
ufw allow $SERVER_PORT/tcp

# Limpeza
log "🧹 Limpeza final..."
rm -f /tmp/mcp_config.env /tmp/deploy_as_user.sh

# Obter URL final
if [[ -n "$DOMAIN" ]]; then
    BASE_URL="http://$DOMAIN:$SERVER_PORT"
else
    BASE_URL="http://$PUBLIC_IP:$SERVER_PORT"
fi

echo
echo -e "${GREEN}"
cat << "EOF"
╔══════════════════════════════════════════════════════════╗
║ ✅ DEPLOY CONCLUÍDO! ║
╚══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

log "📋 Informações do servidor:"
echo -e " 🌐 URL: $BASE_URL"
echo -e " 🔑 Chave API: $MCP_API_KEY"
echo -e " 📊 Health Check: $BASE_URL/health"
echo -e " 📚 Documentação: $BASE_URL/docs"

echo
log "📋 Comandos úteis:"
echo -e " Status: systemctl status letscloud-mcp"
echo -e " Logs: journalctl -u letscloud-mcp -f"
echo -e " Restart: systemctl restart letscloud-mcp"

echo
log "🎉 Servidor pronto para uso!"

echo
warn "⚠️ Salve a API Key: $MCP_API_KEY"
warn "⚠️ Configure seu cliente para usar: $BASE_URL"

# Teste de conectividade
log "🔍 Testando conectividade..."
if curl -f -s "$BASE_URL/health" >/dev/null; then
    log "✅ Health check OK!"
else
    warn "⚠️ Health check falhou. Verifique os logs: journalctl -u letscloud-mcp -f"
fi 