# ⚡ Quick Deploy - LetsCloud MCP Server

## 🚀 **One-Command Installation**

### **1. Create VM on LetsCloud**
```bash
# Using AI itself:
"Create an Ubuntu 22.04 VM with 2GB RAM in São Paulo to host my MCP server"
```

### **2. Run Deploy Script**
```bash
# SSH into VM and execute:
curl -fsSL https://raw.githubusercontent.com/letscloud/letscloud-mcp-server/main/scripts/deploy.sh | bash
```

## 🎯 **What the script does automatically:**

✅ **System:** Updates Ubuntu and installs dependencies  
✅ **Python:** Configures Python 3.11 + virtual environment  
✅ **Project:** Clones repository and installs dependencies  
✅ **Configuration:** Creates .env files and scripts  
✅ **Services:** Configures systemd + nginx + SSL  
✅ **Security:** Firewall + rate limiting + headers  
✅ **Monitoring:** Automatic health checks  

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
sudo systemctl status letscloud-mcp

# View logs in real-time  
sudo journalctl -u letscloud-mcp -f

# Restart service
sudo systemctl restart letscloud-mcp

# Test health
curl http://localhost:8000/health

# List tools (with API key)
curl -H "Authorization: Bearer YOUR_API_KEY" http://localhost:8000/tools
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
- **Open ports 80/443** in provider firewall if necessary
- **Regular backup** of `/home/mcpserver/.env` file

## 🆘 **Troubleshooting:**

```bash
# Service won't start?
sudo journalctl -u letscloud-mcp --no-pager

# Nginx errors?
sudo nginx -t && sudo systemctl status nginx

# Python issues?
sudo -u mcpserver /home/mcpserver/letscloud-mcp-server/venv/bin/python -c "import letscloud_mcp_server; print('OK')"

# Complete redeploy?
curl -fsSL https://raw.githubusercontent.com/letscloud/letscloud-mcp-server/main/scripts/deploy.sh | bash
```

---

**🎯 Deploy in 1 command, MCP server online in minutes!** 