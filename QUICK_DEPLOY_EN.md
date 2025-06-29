# ⚡ Quick Deploy - LetsCloud MCP Server

## 🚀 **One-Command Installation**

### **1. Create VM on LetsCloud**
```bash
# Using AI itself:
"Create an Ubuntu 22.04 VM with 2GB RAM in São Paulo to host my MCP server"
```

### **2. Run Deploy Script**
```bash
# SSH into VM and execute as root:
sudo curl -fsSL https://raw.githubusercontent.com/letscloud-community/letscloud-mcp-server/refs/heads/main/scripts/deploy.sh | bash
```

**💡 New:** Simplified script runs 100% as root - no user creation!

## 🎯 **What the script does automatically:**

✅ **System:** Updates Ubuntu and installs dependencies  
✅ **Python:** Detects Python version + virtual environment  
✅ **Project:** Clones repository to `/opt/letscloud-mcp`  
✅ **Configuration:** Creates .env files and service  
✅ **Services:** Configures systemd service as root  
✅ **Security:** Firewall + credential validation  
✅ **Monitoring:** Integrated health checks  

## 📝 **Information Required:**

During execution, you'll be asked:

1. **🔑 LetsCloud API Token** - Your access token  
2. **🔐 HTTP API Key** - Auto-generated if empty  
3. **🌐 Port** - Default: 8000  
4. **🏠 Domain** - Optional (uses IP if empty)  

## 🎉 **Final Result:**

After 5-10 minutes you'll have:

- **🌐 HTTP Server:** `http://YOUR_IP:8000`
- **📚 Documentation:** `http://YOUR_IP:8000/docs`  
- **💊 Health Check:** `http://YOUR_IP:8000/health`
- **🔐 Secure API** with authentication
- **🔄 Auto-restart** on failure
- **📊 Centralized logs**

## 🔧 **Useful Commands Post-Deploy:**

```bash
# View status
systemctl status letscloud-mcp

# View logs in real-time  
journalctl -u letscloud-mcp -f

# Restart service
systemctl restart letscloud-mcp

# Test health
curl http://localhost:8000/health

# List tools (with API key)
curl -H "Authorization: Bearer YOUR_API_KEY" http://localhost:8000/tools

# View configuration
cat /opt/letscloud-mcp/.env
```

## 🚀 **Use with AI Client:**

### **Claude Desktop:**
```json
{
  "mcpServers": {
    "letscloud-remote": {
      "command": "curl",
      "args": [
        "-X", "POST", 
        "-H", "Authorization: Bearer YOUR_API_KEY",
        "-H", "Content-Type: application/json",
        "http://YOUR_IP:8000/tools/list_servers",
        "-d", "{\"arguments\": {}}"
      ]
    }
  }
}
```

### **Direct HTTP Client:**
```python
import requests

headers = {"Authorization": "Bearer YOUR_API_KEY"}
response = requests.get("http://YOUR_IP:8000/tools", headers=headers)
print(response.json())
```

## ⚠️ **Important Notes:**

- **Save the API Key** shown at the end of deployment
- **Configure DNS** if using custom domain  
- **Open specified port** in provider firewall  
- **Regular backup** of `/opt/letscloud-mcp/.env` file
- **Root execution** - simplified configuration

## 🆘 **Troubleshooting:**

```bash
# Service won't start?
journalctl -u letscloud-mcp --no-pager

# Check configuration?
cat /opt/letscloud-mcp/.env

# Python issues?
cd /opt/letscloud-mcp/letscloud-mcp-server && source venv/bin/activate && python -c "import letscloud_mcp_server; print('OK')"

# Complete redeploy?
sudo curl -fsSL https://raw.githubusercontent.com/letscloud-community/letscloud-mcp-server/refs/heads/main/scripts/deploy.sh | bash
```

---

**🎯 Deploy in 1 command, MCP server online in minutes!** 