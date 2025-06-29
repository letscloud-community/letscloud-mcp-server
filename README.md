# LetsCloud MCP Server

🤖 **Manage your cloud infrastructure through natural AI conversations**

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that lets you manage your LetsCloud servers by simply talking to AI assistants like Claude Desktop, without any technical knowledge required.

## 🌍 Multi-Language Support

- **🇺🇸 [English README](README.md)** (This document)
- **🇧🇷 [Portuguese README](README_PT.md)** - Versão completa em português
- **📖 [Language Support Guide](LANGUAGE_SUPPORT.md)** - Complete bilingual documentation

## 🎯 What You Can Do

Talk naturally to AI and get things done:

- **"Create a server for my online store"** → AI creates it instantly
- **"My website is slow, help fix it"** → AI analyzes and optimizes  
- **"Backup all my servers before the update"** → AI handles everything
- **"My site crashed! Help!"** → AI diagnoses and recovers automatically

No programming. No technical commands. Just natural conversation in **English** or **Portuguese**.

## 🚀 Quick Start

### **Option 1: Local Installation (Desktop)**

#### **1. Get Your LetsCloud API Key**
- Visit [LetsCloud Dashboard](https://my.letscloud.io/profile/client-api)
- Enable and copy API key 

#### **2. Install & Configure Claude Desktop**
- Download [Claude Desktop](https://claude.ai/download)
- Add this to your configuration file:

```json
{
  "mcpServers": {
    "letscloud": {
      "command": "python",
      "args": ["-m", "letscloud_mcp_server"],
      "env": {
        "LETSCLOUD_API_TOKEN": "your-token-here"
      }
    }
  }
}
```

#### **3. Install the MCP Server**
```bash
pip install git+https://github.com/letscloud-community/letscloud-mcp-server.git
```

### **Option 2: Online Deployment (Recommended for Teams)** 🆕

#### **🌐 Deploy to Cloud in 1 Command**
```bash
# Create VM and run as root:
sudo curl -fsSL https://raw.githubusercontent.com/letscloud-community/letscloud-mcp-server/refs/heads/main/scripts/deploy.sh | bash
```

**Result:** Your MCP server running 24/7 online, accessible from anywhere!
**New:** Simplified deployment running 100% as root - no user creation!

📚 **Complete Guides:**
- **📖 [Complete Deployment Guide](DEPLOY_GUIDE_EN.md)** - Step-by-step deployment
- **⚡ [Quick Deploy Guide](QUICK_DEPLOY_EN.md)** - One-command setup
- **🇧🇷 [Guia de Deploy (Português)](DEPLOY_GUIDE.md)** - Guia completo em português

#### **Benefits of Online Deployment:**
- ✅ **24/7 Availability** - Works even when your computer is off
- ✅ **Team Access** - Multiple users can use the same server
- ✅ **Better Performance** - Optimized latency to LetsCloud API
- ✅ **Professional Setup** - SSL, monitoring, auto-restart
- ✅ **Remote Access** - Use from any device, anywhere

### **4. Start Talking!**
Open Claude Desktop and say:
```
"Hi! Show me my current servers and help me manage my infrastructure."
```

## 🛠️ What You Can Manage

### Server Operations
- Create, start, stop, reboot, delete servers
- List servers and get detailed information
- Scale up/down server resources
- Multi-region deployments

### Backup & Recovery
- Create snapshots for data protection
- Automatic backup scheduling
- Quick restore from snapshots
- Emergency recovery procedures

### Security & Access
- SSH key management
- SSL certificate handling
- Access control configuration
- Security monitoring

### Cost Optimization
- Resource usage analysis
- Cost reduction recommendations
- Automatic scaling policies
- Usage monitoring and alerts

## 💬 Example Conversations

### Beginner User
```
You: "I need a website for my small business"
AI: "I'll help you create a professional website. What type of business?"
You: "It's a bakery, I want to show my products and take orders"
AI: "Perfect! Creating a bakery website with online ordering..."
✅ WordPress site created with e-commerce
✅ Payment processing configured  
✅ SSL security enabled
✅ Ready in 10 minutes - $35/month
```

### Emergency Response
```
You: "HELP! My website is down during our biggest sale!"
AI: "🚨 Emergency detected! Investigating immediately..."
🔍 Diagnosed: Server overload from high traffic
⚡ Creating emergency server with 3x capacity
✅ Site restored in 8 minutes with auto-scaling
```

## 🌟 Why Choose LetsCloud MCP Server?

✅ **Zero Technical Knowledge Required** - Just talk naturally  
✅ **Works in English & Portuguese** - Native language support  
✅ **Instant Emergency Response** - AI handles crises automatically  
✅ **Cost Optimization** - AI finds savings opportunities  
✅ **24/7 Monitoring** - Proactive problem prevention  
✅ **Scalable Architecture** - Grows with your business  
✅ **Enterprise Security** - Bank-level data protection  
✅ **Online Deployment** - Remote access from anywhere 🆕

## 🤖 Supported AI Platforms

- **✅ Claude Desktop** (Recommended - Best experience)
- **✅ Cline** (VS Code extension)  
- **✅ Zed Editor**
- **⏳ ChatGPT** (Coming soon to GPT Store)
- **✅ Any MCP-compatible client**
- **🆕 HTTP/WebSocket API** - Remote access via REST API

## 🔧 Installation Options

### **Local Installation**
```bash
# Option A: Install from GitHub (Recommended)
pip install git+https://github.com/letscloud-community/letscloud-mcp-server.git

# Option B: Install from Source  
git clone https://github.com/letscloud-community/letscloud-mcp-server.git
cd letscloud-mcp-server
pip install -e .

# Option C: Install from PyPI (Coming Soon)
pip install letscloud-mcp-server
```

### **Online Deployment** 🆕
```bash
# One-command cloud deployment (as root)
sudo curl -fsSL https://raw.githubusercontent.com/letscloud-community/letscloud-mcp-server/refs/heads/main/scripts/deploy.sh | bash
```

**📚 Complete Deployment Documentation:**
- **🇺🇸 [English Deploy Guide](DEPLOY_GUIDE_EN.md)** - Complete step-by-step
- **🇧🇷 [Portuguese Deploy Guide](DEPLOY_GUIDE.md)** - Guia completo em português
- **⚡ [Quick Deploy (EN)](QUICK_DEPLOY_EN.md)** - One-command setup
- **⚡ [Deploy Rápido (PT)](QUICK_DEPLOY.md)** - Instalação com 1 comando

## 🌍 Language Support

This project provides complete documentation and support in:
- **English** - For international users
- **Português** - Para usuários brasileiros

The AI assistants will automatically detect your language and respond appropriately, adapting:
- Currency (USD vs BRL)
- Payment methods (Credit cards vs PIX)
- Legal compliance (GDPR vs LGPD)
- Business contexts (Global vs Brazilian markets)

**🇧🇷 Para usuários brasileiros:** Acesse a [documentação completa em português](README_PT.md).

## 🚀 Deployment Modes

### **🏠 Local Mode**
- **Best for:** Individual developers, testing, development
- **Installation:** Simple pip install
- **Requirements:** Local Python environment
- **Access:** Local computer only

### **🌐 Online Mode** 🆕  
- **Best for:** Teams, production, 24/7 availability
- **Installation:** One-command cloud deployment
- **Requirements:** VM/VPS with Ubuntu
- **Access:** From anywhere via HTTP/WebSocket API
- **Features:** SSL, monitoring, auto-restart, team access

## 📞 Support & Community

- **🐛 Bug Reports**: [GitHub Issues](https://github.com/letscloud-community/letscloud-mcp-server/issues)
- **💬 Questions**: [GitHub Discussions](https://github.com/letscloud-community/letscloud-mcp-server/discussions)
- **🌐 LetsCloud Support**: [support@letscloud.io](mailto:support@letscloud.io)
- **🌍 Multi-language**: English and Portuguese support available

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io) by Anthropic
- [LetsCloud](https://letscloud.io) for the infrastructure API
- The open source community for inspiration and support

