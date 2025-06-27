# LetsCloud MCP Server - User Guide

This guide shows how to use the LetsCloud MCP Server through AI interfaces like Claude Desktop, ChatGPT, and other intelligent assistants to manage your infrastructure using natural language.

## 🤖 What can you do?

With the LetsCloud MCP Server integrated into your AI, you can:

- **"Create a server for my online store"** → AI creates it automatically
- **"My website is slow, what should I do?"** → AI analyzes and optimizes
- **"Backup everything before the update"** → AI performs complete backup
- **"I need my site to handle more visitors"** → AI scales the infrastructure
- **"My site went down, help!"** → AI diagnoses and resolves emergencies

## 🔧 Configuration by Platform

### Claude Desktop (Recommended)

1. **Get your LetsCloud API Key**
   ```
   Visit: https://cloud.letscloud.io/account/api
   Copy your token: let_1234567890abcdef...
   ```

2. **Configure Claude Desktop**
   ```json
   {
     "mcpServers": {
       "letscloud": {
         "command": "python",
         "args": ["-m", "letscloud_mcp_server"],
         "env": {
           "LETSCLOUD_API_TOKEN": "let_your-token-here"
         }
       }
     }
   }
   ```

3. **Configuration file location:**
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/claude/claude_desktop_config.json`

4. **Restart Claude Desktop** after saving the configuration

### OpenAI ChatGPT (GPT Store)

1. **Pending approval** - Coming soon to GPT Store
2. **Enterprise version**: Contact support for custom integration

### Other AI Assistants

The MCP Server works with any AI that supports the MCP protocol:
- **Cline** (VS Code)
- **Zed Editor**
- **Other MCP clients**

## 💬 How to Use - Conversation Examples

### Scenario 1: Beginner User

**You:** "Hi! I need a server for my WordPress blog"

**AI:** "Sure! I'll create an optimized server for WordPress. A few quick questions:
- How many visitors per month do you expect?
- Do you already have a registered domain?
- Do you want automatic WordPress installation?"

**You:** "About 500 visitors, I have a domain, yes I want automatic"

**AI:** "Perfect! Creating now:
✅ Server created: 2GB RAM, Ubuntu 22.04
✅ WordPress installed and configured  
✅ Free SSL activated
✅ Daily backup configured
💰 Cost: $25/month
🌐 IP: 165.232.123.45
⏱️ Ready in 5 minutes!"

### Scenario 2: Growing E-commerce

**You:** "My online store is getting slow, I have 1000 visitors per day now"

**AI:** "I can see you need to scale! Your growth is excellent. I'll implement:

🏗️ **New Architecture:**
- Load Balancer to distribute traffic
- 2 web servers for redundancy  
- Dedicated database server
- Caching system for speed

💰 **Cost:** $65/month (vs $35 current)
🚀 **Benefit:** Supports up to 10,000 visitors/day
⚡ **Speed:** 3x faster
🛡️ **Availability:** 99.9%

Should I implement this now?"

### Scenario 3: Emergency

**You:** "HELP! My site has been down for 20 minutes!"

**AI:** "🚨 **EMERGENCY DETECTED** - Starting immediate diagnosis...

🔍 **Diagnosis:**
- Main server not responding ❌
- Issue: Hardware failure
- Backup available: 2 hours ago ✅

⚡ **Recovery in progress:**
- 00:00 Creating emergency server
- 00:03 Restoring backup  
- 00:07 Redirecting DNS
- 00:09 ✅ SITE WORKING!

**Total:** 9 minutes downtime
**Prevention:** Configured high availability to prevent future failures"

## 🎯 Use Cases by Business Type

### 🍕 Restaurant - Delivery
**You:** "I need a website for my restaurant delivery"
**AI creates:** Site with menu, online orders, WhatsApp integration, payment processing

### 🎓 Online School  
**You:** "I want an online course platform"
**AI creates:** Moodle configured, student area, video uploads, certificates

### ⚖️ Law Firm
**You:** "I need a professional website for my law office"
**AI creates:** Corporate site, client area, secure uploads, GDPR compliance

### 📸 Photographer
**You:** "I want to showcase my portfolio and sell photos"
**AI creates:** Professional gallery, image protection, integrated e-commerce

## 🔒 Secure Configuration

### Environment Variables (Optional)

For advanced features, configure:

```bash
# Required
LETSCLOUD_API_TOKEN="let_your-token-here"

# Optional - For enhanced AI features
OPENAI_API_KEY="sk-your-openai-token"      # For intelligent analysis
ANTHROPIC_API_KEY="sk-ant-your-token"      # For recommendation comparison

# Optional - For alerts
ALERT_EMAIL="admin@yourdomain.com"         # Receive email alerts
SLACK_WEBHOOK_URL="https://hooks.slack..." # Slack notifications
```

### Getting the Keys

**LetsCloud API (Required):**
1. Visit https://cloud.letscloud.io/account/api
2. Click "Generate New Key"
3. Copy the token starting with `let_`

**OpenAI (Optional):**
1. Visit https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key starting with `sk-`

**Anthropic Claude (Optional):**
1. Visit https://console.anthropic.com/
2. Go to "API Keys" → "Create Key"
3. Copy the key starting with `sk-ant-`

## 💡 Intelligent Features

### With OpenAI Integration
- **Intelligent log analysis:** "Why is my site slow today?"
- **Automatic optimization:** "Reduce my costs without losing performance"
- **Architecture planning:** "I need to support 50,000 users"

### With Claude Integration  
- **Solution comparison:** Receives multiple recommendations and chooses the best
- **Risk analysis:** Evaluates impacts before making changes
- **Automatic documentation:** Generates detailed operation reports

## 🚀 Getting Started

1. **Configure your AI platform** (Claude Desktop recommended)
2. **Add your LetsCloud key** to the configuration
3. **Restart the AI application**
4. **Test with:** "List my current servers"
5. **Start using naturally:** "I need a server for..."

## 📞 Support

- **Technical documentation:** For developers who want to integrate
- **LetsCloud support:** For account and billing questions
- **MCP Community:** For questions about the MCP protocol

## 🎉 Advantages

✅ **Zero technical knowledge required**
✅ **Natural language communication**
✅ **Automatic execution of complex tasks**
✅ **24/7 intelligent monitoring**
✅ **Continuous cost optimization**
✅ **Instant emergency support**
✅ **Automatic scalability**
✅ **Automated backups and security**

Start now by talking naturally with your AI about your infrastructure needs! 