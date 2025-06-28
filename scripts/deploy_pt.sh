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
║                 Script de Instalação Automática         ║
╚══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Verificar se está rodando como root
if [[ $EUID -eq 0 ]]; then
    warn "⚠️  Detectado que você está executando como root!"
    echo "Por segurança, é recomendado executar como usuário não-root."
    echo
    read -p "🤔 Deseja criar automaticamente um usuário 'mcpserver' e continuar? (s/n): " create_user
    
    if [[ "$create_user" =~ ^[SsYy]$ ]]; then
        log "👤 Criando usuário 'mcpserver'..."
        
        # Verificar se usuário já existe
        if id "mcpserver" &>/dev/null; then
            log "👤 Usuário 'mcpserver' já existe!"
        else
            # Criar usuário
            useradd -m -s /bin/bash mcpserver
            log "✅ Usuário 'mcpserver' criado com sucesso!"
        fi
        
        # Adicionar ao grupo sudo se não estiver
        usermod -aG sudo mcpserver
        
        # Configurar sudo sem senha para este script
        echo "mcpserver ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/mcpserver-temp
        
        log "🔄 Mudando para usuário 'mcpserver' e continuando..."
        
        # Primeiro solicitar configurações como root
        echo
        log "📋 Configuração inicial (como root)..."
        echo
        
        read -p "🔑 Token da API LetsCloud: " LETSCLOUD_API_TOKEN
        while [[ -z "$LETSCLOUD_API_TOKEN" ]]; do
            read -p "🔑 Token da API LetsCloud (obrigatório): " LETSCLOUD_API_TOKEN
        done
        
        read -p "🔐 Chave da API HTTP (deixe vazio para gerar): " MCP_API_KEY
        read -p "🌐 Porta do servidor [8000]: " SERVER_PORT
        SERVER_PORT=${SERVER_PORT:-8000}
        read -p "🏠 Domínio (opcional, deixe vazio para usar IP): " DOMAIN
        
        # Gerar chave API se não fornecida
        if [[ -z "$MCP_API_KEY" ]]; then
            MCP_API_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || openssl rand -base64 32)
            log "🔐 Chave API gerada automaticamente: $MCP_API_KEY"
        fi
        
        # Salvar configurações em arquivo temporário
        cat > /tmp/mcp_config.env << EOF
LETSCLOUD_API_TOKEN="$LETSCLOUD_API_TOKEN"
MCP_API_KEY="$MCP_API_KEY"
SERVER_PORT="$SERVER_PORT"
DOMAIN="$DOMAIN"
SKIP_CONFIG=true
EOF
        
        # Copiar o script original para /tmp
        cp "$0" /tmp/deploy_as_user.sh
        chmod +x /tmp/deploy_as_user.sh
        
        # Executar como mcpserver carregando as configurações
        exec sudo -u mcpserver -i bash -c "source /tmp/mcp_config.env && /tmp/deploy_as_user.sh"
        
        # Esta linha nunca será alcançada devido ao exec
        exit 0
    else
        echo
        warn "Para executar manualmente como usuário não-root:"
        echo "1. Criar usuário: useradd -m -s /bin/bash mcpserver"
        echo "2. Adicionar ao sudo: usermod -aG sudo mcpserver"  
        echo "3. Mudar usuário: su - mcpserver"
        echo "4. Executar script: curl -fsSL https://raw.githubusercontent.com/letscloud-community/letscloud-mcp-server/refs/heads/main/scripts/deploy_pt.sh | bash"
        exit 1
    fi
fi

# Carregar configurações se disponíveis (para execução via smart deploy)
if [[ -f "/tmp/mcp_config.env" && "$SKIP_CONFIG" != "true" ]]; then
    log "📥 Carregando configurações do smart deploy..."
    source /tmp/mcp_config.env
    log "✅ Configurações carregadas com sucesso"
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
    get_input "🔐 Chave da API HTTP (deixe vazio para gerar)" "MCP_API_KEY"
    get_input "🌐 Porta do servidor" "SERVER_PORT" "8000"
    get_input "🏠 Domínio (opcional, deixe vazio para usar IP)" "DOMAIN"

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
sudo apt update && sudo apt upgrade -y

# Instalar dependências básicas
log "🔧 Instalando dependências..."

# Auto-detectar versão do Python
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '3\.\d+' | head -1)
if [[ -z "$PYTHON_VERSION" ]]; then
    PYTHON_VERSION="3.10"  # Fallback
fi
log "🐍 Python $PYTHON_VERSION detectado"

sudo apt install -y \
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
    sudo -u mcpserver git clone https://github.com/letscloud-community/letscloud-mcp-server.git "$PROJECT_DIR"
fi

# Configurar ambiente Python
log "🐍 Configurando ambiente Python..."
cd "$PROJECT_DIR"

# Criar ambiente virtual
if [[ ! -d "venv" ]]; then
    sudo -u mcpserver python3 -m venv venv
fi

# Ativar venv e instalar dependências
sudo -u mcpserver bash -c "
    source venv/bin/activate
    pip install --upgrade pip
    pip install -e .
"

# Criar arquivo de configuração
log "⚙️ Criando arquivo de configuração..."

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

log "✅ Arquivo de configuração criado em $MCP_HOME/.env"

# Exibir informações finais
echo
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║ ✅ DEPLOY CONCLUÍDO! ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo

# Definir valores padrão para as variáveis se não estiverem definidas
SERVER_PORT=${SERVER_PORT:-8000}
MCP_API_KEY=${MCP_API_KEY:-"ERRO-CHAVE-NAO-CONFIGURADA"}
LETSCLOUD_API_TOKEN=${LETSCLOUD_API_TOKEN:-"ERRO-TOKEN-NAO-CONFIGURADO"}

# Debug: verificar se as variáveis estão definidas corretamente
if [[ "$MCP_API_KEY" == "ERRO-CHAVE-NAO-CONFIGURADA" ]]; then
    warn "⚠️ Chave API não foi configurada corretamente!"
    log "🔄 Gerando nova chave API..."
    MCP_API_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || openssl rand -base64 32)
    log "🔐 Nova chave API gerada: $MCP_API_KEY"
fi

# Obter IP público
PUBLIC_IP=$(curl -s ifconfig.me || echo "localhost")

log "📋 Informações do servidor:"
echo -e " 🌐 URL: http://$PUBLIC_IP:$SERVER_PORT"
echo -e " 🔑 Chave API: $MCP_API_KEY"
echo -e " 📊 Health Check: http://$PUBLIC_IP:$SERVER_PORT/health"
echo -e " 📚 Documentação: http://$PUBLIC_IP:$SERVER_PORT/docs"
echo

log "📋 Comandos úteis:"
echo -e " Status: sudo systemctl status letscloud-mcp"
echo -e " Logs: sudo journalctl -u letscloud-mcp -f"
echo -e " Restart: sudo systemctl restart letscloud-mcp"
echo

log "🎉 Servidor pronto para uso!"
echo
echo -e "${YELLOW}⚠️ Salve a API Key: $MCP_API_KEY${NC}"
echo -e "${YELLOW}⚠️ Configure seu cliente para usar: http://$PUBLIC_IP:$SERVER_PORT${NC}"

# Limpeza de arquivos temporários (se executado via root switch)
sudo rm -f /etc/sudoers.d/mcpserver-temp 2>/dev/null || true
rm -f /tmp/deploy_as_user.sh 2>/dev/null || true
rm -f /tmp/mcp_config.env 2>/dev/null || true 