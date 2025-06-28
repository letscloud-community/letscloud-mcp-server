# 🚀 Deployment Guide - Host LetsCloud MCP Server Online

## 📋 **Overview**

This guide shows how to configure a VM and host the LetsCloud MCP Server online, enabling remote access via HTTP/WebSocket instead of local only.

---

## 🎯 **Hosting Options**

### **1. LetsCloud (Recommended)**
- ✅ **Native infrastructure** - Best integration  
- ✅ **Specialized support** - Expert technical team
- ✅ **Optimized performance** - Minimal API latency
- ✅ **Competitive pricing** - Starting at $15/month

### **2. Other Providers**
- **DigitalOcean** - $6/month (basic)
- **AWS EC2** - $3-10/month (t3.micro)
- **Google Cloud** - $5-15/month
- **Azure** - $4-12/month

---

## 🛠️ **Step 1: Create VM on LetsCloud**

### **Via Web Interface:**
1. Access [LetsCloud Dashboard](https://my.letscloud.io)
2. Click **"Create Instance"**
3. Configure:
   - **OS:** Ubuntu 22.04 LTS
   - **Plan:** Standard 2GB (2 vCPU, 2GB RAM)
   - **Location:** São Paulo (best latency)
   - **Name:** `letscloud-mcp-server`

### **Via AI (Using MCP itself):**
```
"Create an Ubuntu 22.04 VM with 2GB RAM in São Paulo to host my MCP server"
```

---

## 🔧 **Step 2: Configure the Server**

### **1. Connect via SSH**
```bash
# Copy the created VM IP
ssh root@YOUR_VM_IP

# Update system
apt update && apt upgrade -y
```

### **2. Install Dependencies**
```bash
# Install Python 3.11+
apt install python3.11 python3.11-pip python3.11-venv git nginx certbot python3-certbot-nginx -y

# Create dedicated user
useradd -m -s /bin/bash mcpserver
usermod -aG sudo mcpserver
```

### **3. Configure Project**
```bash
# Switch to dedicated user
su - mcpserver

# Clone repository
git clone https://github.com/letscloud-community/letscloud-mcp-server.git
cd letscloud-mcp-server

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .
pip install fastapi uvicorn[standard] python-multipart
```

---

## 🔐 **Step 3: Configure Environment Variables**

### **1. Configuration File**
```bash
# Create configuration file
nano /home/mcpserver/.env
```

### **2. Required Variables**
```env
# LetsCloud API Token
LETSCLOUD_API_TOKEN=your_token_here

# Security key for HTTP API
MCP_API_KEY=generate_a_secure_random_key

# Server settings
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=production

# Logs
LOG_LEVEL=INFO
```

### **3. Generate Secure Key**
```bash
# Generate random key
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 🌐 **Step 4: Configure HTTP Server**

### **1. Create Startup Script**
```bash
nano /home/mcpserver/start_server.py
```

```python
#!/usr/bin/env python3
"""
LetsCloud MCP HTTP Server startup script
"""
import os
import sys
import asyncio
from pathlib import Path

# Add project to PATH
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from letscloud_mcp_server.http_server import run_server

async def main():
    """Start HTTP server."""
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv("/home/mcpserver/.env")
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Starting LetsCloud MCP Server on {host}:{port}")
    await run_server(host, port)

if __name__ == "__main__":
    asyncio.run(main())
```

### **2. Make Executable**
```bash
chmod +x /home/mcpserver/start_server.py
```

---

## 🔒 **Step 5: Configure HTTPS (SSL)**

### **1. Configure Nginx (Reverse Proxy)**
```bash
sudo nano /etc/nginx/sites-available/letscloud-mcp
```

```nginx
server {
    listen 80;
    server_name your-domain.com;  # or public IP

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

### **2. Enable Site**
```bash
sudo ln -s /etc/nginx/sites-available/letscloud-mcp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### **3. Configure SSL (if you have a domain)**
```bash
sudo certbot --nginx -d your-domain.com
```

---

## 🔄 **Step 6: Configure Systemd Service**

### **1. Create Service File**
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

### **2. Enable Service**
```bash
sudo systemctl daemon-reload
sudo systemctl enable letscloud-mcp
sudo systemctl start letscloud-mcp

# Check status
sudo systemctl status letscloud-mcp
```

---

## 🧪 **Step 7: Test Installation**

### **1. Local Test**
```bash
# Inside the VM
curl http://localhost:8000/health
```

### **2. Remote Test**
```bash
# From your computer
curl http://YOUR_VM_IP/health

# Or with HTTPS (if configured)
curl https://your-domain.com/health
```

### **3. Authentication Test**
```bash
curl -H "Authorization: Bearer YOUR_MCP_API_KEY" \
     http://YOUR_VM_IP/tools
```

---

## 🔧 **Step 8: Configure Remote Client**

### **1. Claude Desktop (HTTP)**
```json
{
  "mcpServers": {
    "letscloud-remote": {
      "command": "curl",
      "args": [
        "-X", "POST",
        "-H", "Authorization: Bearer YOUR_MCP_API_KEY",
        "-H", "Content-Type: application/json",
        "http://YOUR_VM_IP/tools/{tool_name}",
        "-d", "{arguments}"
      ]
    }
  }
}
```

### **2. Direct HTTP Client**
```python
import requests

# Configuration
API_BASE = "http://YOUR_VM_IP"
API_KEY = "YOUR_MCP_API_KEY"
headers = {"Authorization": f"Bearer {API_KEY}"}

# List tools
response = requests.get(f"{API_BASE}/tools", headers=headers)
tools = response.json()

# Call tool
data = {"arguments": {"server_id": 123}}
response = requests.post(
    f"{API_BASE}/tools/get_server", 
    json=data, 
    headers=headers
)
result = response.json()
```

---

## 📊 **Step 9: Monitoring and Logs**

### **1. View Logs**
```bash
# Service logs
sudo journalctl -u letscloud-mcp -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### **2. Performance Monitoring**
```bash
# CPU/RAM usage
htop

# Active connections
netstat -tulpn | grep :8000

# Service status
systemctl status letscloud-mcp nginx
```

### **3. Health Check Script**
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

## 🔐 **Step 10: Additional Security**

### **1. Firewall**
```bash
# Configure UFW
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
```

### **2. Fail2Ban (Attack protection)**
```bash
sudo apt install fail2ban -y
```

### **3. Automatic Updates**
```bash
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure unattended-upgrades
```

---

## 🚀 **Usage After Deployment**

### **1. Available Endpoints**
- **GET** `/` - Basic health check
- **GET** `/health` - Detailed health check  
- **GET** `/tools` - List MCP tools
- **POST** `/tools/{name}` - Execute tool
- **WebSocket** `/mcp` - Native MCP connection
- **GET** `/docs` - Interactive documentation

### **2. API Usage Example**
```bash
# List your LetsCloud instances
curl -X POST \
  -H "Authorization: Bearer YOUR_MCP_API_KEY" \
  -H "Content-Type: application/json" \
  http://YOUR_VM_IP/tools/list_servers \
  -d '{"arguments": {}}'
```

### **3. Configure in AI Clients**
```json
{
  "mcpServers": {
    "letscloud-remote": {
      "endpoint": "http://YOUR_VM_IP",
      "apiKey": "YOUR_MCP_API_KEY",
      "type": "http"
    }
  }
}
```

---

## 💰 **Estimated Costs**

### **LetsCloud (Recommended)**
- **Standard 2GB:** $25/month
- **Standard 4GB:** $45/month (for high demand)
- **Domain:** $40/year (optional)

### **Benefits vs Local**
- ✅ **24/7 Availability** - No dependency on your PC
- ✅ **Access from anywhere** - Work from any device
- ✅ **Better performance** - Low latency to LetsCloud API
- ✅ **Automatic backup** - Your data protected
- ✅ **Multiple users** - Entire team can use

---

## 🎉 **Conclusion**

After following this guide, you will have:

✅ **LetsCloud MCP Server** running 24/7 in the cloud  
✅ **HTTP/WebSocket API** for remote access  
✅ **HTTPS/SSL** configured for security  
✅ **Monitoring** and logs configured  
✅ **Automatic backup** of the system  

**🚀 Your server will be ready for professional use!**

---

## 📞 **Support**

- **🐛 Issues:** [GitHub Issues](https://github.com/letscloud-community/letscloud-mcp-server/issues)
- **💬 Discussions:** [GitHub Discussions](https://github.com/letscloud-community/letscloud-mcp-server/discussions)
- **🌐 LetsCloud:** [support@letscloud.io](mailto:support@letscloud.io)

---

*Last updated: January 2025* 