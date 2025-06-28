# 🚀 Guia de Deploy - Hospedar LetsCloud MCP Server Online

## 📋 **Visão Geral**

Este guia mostra como configurar uma VM e hospedar o LetsCloud MCP Server online, permitindo acesso remoto via HTTP/WebSocket ao invés de apenas local.

---

## 🎯 **Opções de Hospedagem**

### **1. LetsCloud (Recomendado)**
- ✅ **Própria infraestrutura** - Melhor integração  
- ✅ **Suporte nativo** - Equipe técnica especializada
- ✅ **Performance otimizada** - Latência mínima API
- ✅ **Custo competitivo** - A partir de R$ 15/mês

### **2. Outros Provedores**
- **DigitalOcean** - $6/mês (básico)
- **AWS EC2** - $3-10/mês (t3.micro)
- **Google Cloud** - $5-15/mês
- **Azure** - $4-12/mês

---

## 🛠️ **Passo 1: Criar VM no LetsCloud**

### **Via Interface Web:**
1. Acesse [LetsCloud Dashboard](https://my.letscloud.io)
2. Clique em **"Criar Instância"**
3. Configure:
   - **OS:** Ubuntu 22.04 LTS
   - **Plano:** Standard 2GB (2 vCPU, 2GB RAM)
   - **Localização:** São Paulo (melhor latência)
   - **Nome:** `letscloud-mcp-server`

### **Via AI (Usando o próprio MCP):**
```
"Crie uma VM Ubuntu 22.04 com 2GB RAM em São Paulo para hospedar meu servidor MCP"
```

---

## 🔧 **Passo 2: Configurar o Servidor**

### **1. Conectar via SSH**
```bash
# Copie o IP da VM criada
ssh root@SEU_IP_VM

# Atualizar sistema
apt update && apt upgrade -y
```

### **2. Instalar Dependências**
```bash
# Instalar Python 3.11+
apt install python3.11 python3.11-pip python3.11-venv git nginx certbot python3-certbot-nginx -y

# Criar usuário dedicado
useradd -m -s /bin/bash mcpserver
usermod -aG sudo mcpserver
```

### **3. Configurar Projeto**
```bash
# Trocar para usuário dedicado
su - mcpserver

# Clonar repositório
git clone https://github.com/letscloud/letscloud-mcp-server.git
cd letscloud-mcp-server

# Criar ambiente virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -e .
pip install fastapi uvicorn[standard] python-multipart
```

---

## 🔐 **Passo 3: Configurar Variáveis de Ambiente**

### **1. Arquivo de Configuração**
```bash
# Criar arquivo de configuração
nano /home/mcpserver/.env
```

### **2. Variáveis Necessárias**
```env
# Token da API LetsCloud
LETSCLOUD_API_TOKEN=seu_token_aqui

# Chave de segurança para API HTTP
MCP_API_KEY=gere_uma_chave_segura_aleatoria

# Configurações do servidor
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=production

# Logs
LOG_LEVEL=INFO
```

### **3. Gerar Chave Segura**
```bash
# Gerar chave aleatória
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 🌐 **Passo 4: Configurar Servidor HTTP**

### **1. Criar Script de Inicialização**
```bash
nano /home/mcpserver/start_server.py
```

```python
#!/usr/bin/env python3
"""
Script de inicialização do LetsCloud MCP HTTP Server
"""
import os
import sys
import asyncio
from pathlib import Path

# Adicionar o projeto ao PATH
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from letscloud_mcp_server.http_server import run_server

async def main():
    """Iniciar servidor HTTP."""
    # Carregar variáveis de ambiente
    from dotenv import load_dotenv
    load_dotenv("/home/mcpserver/.env")
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Starting LetsCloud MCP Server on {host}:{port}")
    await run_server(host, port)

if __name__ == "__main__":
    asyncio.run(main())
```

### **2. Tornar Executável**
```bash
chmod +x /home/mcpserver/start_server.py
```

---

## 🔒 **Passo 5: Configurar HTTPS (SSL)**

### **1. Configurar Nginx (Reverse Proxy)**
```bash
sudo nano /etc/nginx/sites-available/letscloud-mcp
```

```nginx
server {
    listen 80;
    server_name seu-dominio.com;  # ou IP público

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

### **2. Ativar Site**
```bash
sudo ln -s /etc/nginx/sites-available/letscloud-mcp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### **3. Configurar SSL (se tiver domínio)**
```bash
sudo certbot --nginx -d seu-dominio.com
```

---

## 🔄 **Passo 6: Configurar Serviço Systemd**

### **1. Criar Arquivo de Serviço**
```bash
sudo nano /etc/systemd/system/letscloud-mcp.service
```

```ini
[Unit]
Description=LetsCloud MCP Server
After=network.target

[Service]
Type=simple
User=mcpserver
Group=mcpserver
WorkingDirectory=/home/mcpserver/letscloud-mcp-server
Environment=PATH=/home/mcpserver/letscloud-mcp-server/venv/bin
ExecStart=/home/mcpserver/letscloud-mcp-server/venv/bin/python /home/mcpserver/start_server.py
Restart=always
RestartSec=10

# Logs
StandardOutput=journal
StandardError=journal
SyslogIdentifier=letscloud-mcp

[Install]
WantedBy=multi-user.target
```

### **2. Ativar Serviço**
```bash
sudo systemctl daemon-reload
sudo systemctl enable letscloud-mcp
sudo systemctl start letscloud-mcp

# Verificar status
sudo systemctl status letscloud-mcp
```

---

## 🧪 **Passo 7: Testar a Instalação**

### **1. Teste Local**
```bash
# Dentro da VM
curl http://localhost:8000/health
```

### **2. Teste Remoto**
```bash
# Do seu computador
curl http://SEU_IP_VM/health

# Ou com HTTPS (se configurado)
curl https://seu-dominio.com/health
```

### **3. Teste de Autenticação**
```bash
curl -H "Authorization: Bearer SUA_MCP_API_KEY" \
     http://SEU_IP_VM/tools
```

---

## 🔧 **Passo 8: Configurar Cliente Remoto**

### **1. Claude Desktop (HTTP)**
```json
{
  "mcpServers": {
    "letscloud-remote": {
      "command": "curl",
      "args": [
        "-X", "POST",
        "-H", "Authorization: Bearer SUA_MCP_API_KEY",
        "-H", "Content-Type: application/json",
        "http://SEU_IP_VM/tools/{tool_name}",
        "-d", "{arguments}"
      ]
    }
  }
}
```

### **2. Client HTTP Direto**
```python
import requests

# Configuração
API_BASE = "http://SEU_IP_VM"
API_KEY = "SUA_MCP_API_KEY"
headers = {"Authorization": f"Bearer {API_KEY}"}

# Listar ferramentas
response = requests.get(f"{API_BASE}/tools", headers=headers)
tools = response.json()

# Chamar ferramenta
data = {"arguments": {"server_id": 123}}
response = requests.post(
    f"{API_BASE}/tools/get_server", 
    json=data, 
    headers=headers
)
result = response.json()
```

---

## 📊 **Passo 9: Monitoramento e Logs**

### **1. Visualizar Logs**
```bash
# Logs do serviço
sudo journalctl -u letscloud-mcp -f

# Logs do Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### **2. Monitoramento de Performance**
```bash
# Uso de CPU/RAM
htop

# Conexões ativas
netstat -tulpn | grep :8000

# Status do serviço
systemctl status letscloud-mcp nginx
```

### **3. Script de Health Check**
```bash
nano /home/mcpserver/health_check.sh
```

```bash
#!/bin/bash
# Health check script

response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)

if [ $response = "200" ]; then
    echo "✅ MCP Server is healthy"
    exit 0
else
    echo "❌ MCP Server is down (HTTP $response)"
    # Restart service
    sudo systemctl restart letscloud-mcp
    exit 1
fi
```

---

## 🔐 **Passo 10: Segurança Adicional**

### **1. Firewall**
```bash
# Configurar UFW
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
```

### **2. Fail2Ban (Proteção contra ataques)**
```bash
sudo apt install fail2ban -y
```

### **3. Atualizações Automáticas**
```bash
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure unattended-upgrades
```

---

## 🚀 **Uso Após Deploy**

### **1. Endpoints Disponíveis**
- **GET** `/` - Health check básico
- **GET** `/health` - Health check detalhado  
- **GET** `/tools` - Listar ferramentas MCP
- **POST** `/tools/{nome}` - Executar ferramenta
- **WebSocket** `/mcp` - Conexão MCP nativa
- **GET** `/docs` - Documentação interativa

### **2. Exemplo de Uso via API**
```bash
# Listar suas instâncias LetsCloud
curl -X POST \
  -H "Authorization: Bearer SUA_MCP_API_KEY" \
  -H "Content-Type: application/json" \
  http://SEU_IP_VM/tools/list_servers \
  -d '{"arguments": {}}'
```

### **3. Configurar em Clients AI**
```json
{
  "mcpServers": {
    "letscloud-remote": {
      "endpoint": "http://SEU_IP_VM",
      "apiKey": "SUA_MCP_API_KEY",
      "type": "http"
    }
  }
}
```

---

## 💰 **Custos Estimados**

### **LetsCloud (Recomendado)**
- **Standard 2GB:** R$ 25/mês
- **Standard 4GB:** R$ 45/mês (para alta demanda)
- **Domínio:** R$ 40/ano (opcional)

### **Benefícios vs Local**
- ✅ **Disponibilidade 24/7** - Sem depender do seu PC
- ✅ **Acesso de qualquer lugar** - Trabalhe de qualquer dispositivo
- ✅ **Performance melhor** - Latência baixa para LetsCloud API
- ✅ **Backup automático** - Seus dados protegidos
- ✅ **Múltiplos usuários** - Equipe toda pode usar

---

## 🎉 **Conclusão**

Após seguir este guia, você terá:

✅ **LetsCloud MCP Server** rodando 24/7 na nuvem  
✅ **API HTTP/WebSocket** para acesso remoto  
✅ **HTTPS/SSL** configurado para segurança  
✅ **Monitoramento** e logs configurados  
✅ **Backup automático** do sistema  

**🚀 Seu servidor estará pronto para uso profissional!**

---

## 📞 **Suporte**

- **🐛 Issues:** [GitHub Issues](https://github.com/letscloud/letscloud-mcp-server/issues)
- **💬 Discussões:** [GitHub Discussions](https://github.com/letscloud/letscloud-mcp-server/discussions)
- **🌐 LetsCloud:** [support@letscloud.io](mailto:support@letscloud.io)

---

*Última atualização: Janeiro 2025* 