# How to Use LetsCloud MCP Server with AI

Complete guide to configure and use the LetsCloud MCP Server on different AI platforms.

## 🎯 Overview

The LetsCloud MCP Server allows you to manage your server infrastructure through **natural conversations** with AI. No need to know programming or technical commands - just talk normally!

### What you can do:
- **"Create a server for my online store"**
- **"My website is slow, help me fix it"** 
- **"Backup all my servers"**
- **"I need my site to handle more traffic"**
- **"Help! My site went down!"**

## 🔧 Configuration by Platform

### 1. Claude Desktop (Easiest - Recommended)

#### Step 1: Install Claude Desktop
- Download at: https://claude.ai/download
- Install and create an account

#### Step 2: Get your LetsCloud key
1. Visit: https://cloud.letscloud.io/account/api
2. Click "Generate New API Key"
3. Copy the token (starts with `let_`)

#### Step 3: Configure the MCP Server
1. **Find the configuration file:**
   - **Windows**: Open `%APPDATA%\Claude\claude_desktop_config.json`
   - **Mac**: Open `~/Library/Application Support/Claude/claude_desktop_config.json`  
   - **Linux**: Open `~/.config/claude/claude_desktop_config.json`

2. **Paste this configuration:**
   ```json
   {
     "mcpServers": {
       "letscloud": {
         "command": "python",
         "args": ["-m", "letscloud_mcp_server"],
         "env": {
           "LETSCLOUD_API_TOKEN": "paste-your-token-here"
         }
       }
     }
   }
   ```

3. **Replace** `paste-your-token-here` with your actual token

#### Step 4: Install the MCP Server
Open terminal/command prompt and run:
```bash
pip install letscloud-mcp-server
```

#### Step 5: Restart and Test
1. Close Claude Desktop completely
2. Open again
3. Type: **"List my current servers"**
4. If it worked, you'll see your server list! 🎉

### 2. OpenAI ChatGPT (Future)

**Status:** In development
- Awaiting approval on GPT Store
- For enterprises: Contact support for custom integration

### 3. Other MCP Clients

The MCP Server works with any application that supports the MCP protocol:
- **Cline** (VS Code extension)
- **Zed Editor**
- **Continue** (VS Code)
- Any MCP-compatible client

## 💬 How to Talk to AI

### Natural Language - Real Examples

#### For Beginners:
```
You: "Hi! I'm new here and need a server for my website"

AI: "Hello! I'll help you create your first server. A few questions:
- What type of website do you want to create?
- How many visitors do you expect per month?
- What's your budget?"

You: "It's a personal blog, about 100 visitors per month, budget $50"

AI: "Perfect! I'll create a basic server ideal for you:
✅ Server created with 1GB RAM
✅ WordPress installed automatically
✅ Free SSL configured
✅ Cost: $25/month (within budget!)
Want me to configure your domain too?"
```

#### For E-commerce:
```
You: "I have an online store that's growing fast, sometimes it gets slow"

AI: "That's great that it's growing! Let me analyze your situation:
- How many unique visitors per day do you have now?
- How many products in your store?
- When do you notice the slowness most?"

You: "About 500 visitors per day, 200 products, gets slow in the evening"

AI: "I identified the problem! You need to scale. I'll implement:
🏗️ Load balancer to distribute traffic
🚀 Additional server for peak hours  
⚡ Smart caching for products
💰 Cost: +$45/month, but 3x faster site
Should I implement this now?"
```

#### For Emergencies:
```
You: "HELP! My site went down and I have customers waiting!"

AI: "🚨 EMERGENCY! I'm already investigating...

🔍 Diagnosis in 30 seconds:
- Main server: Not responding ❌
- Cause: CPU overload
- Solution: Emergency migration ⚡

🔄 Recovering NOW:
- Creating emergency server (2 min)
- Restoring latest backup (3 min)  
- Redirecting traffic (1 min)

✅ RESOLVED! Your site is back online.
Total downtime: 6 minutes
Setting up protection against future overloads."
```

## 🛠️ Types of Requests That Work

### Server Creation
- "Create a server for WordPress"
- "I need a server for my Magento store"
- "I want to host a Node.js application"
- "Create a development server"

### Management
- "List all my servers"
- "Which server is using the most resources?"
- "Restart the online store server"
- "Increase memory on the main server"

### Backups and Security
- "Backup everything now"
- "When was the last backup?"
- "Restore the site from yesterday"
- "Set up automatic weekly backup"

### Monitoring
- "How is server performance?"
- "My site is slow, why?"
- "Which servers are overloaded?"
- "I need alerts when something goes wrong"

### Optimization
- "How can I reduce costs?"
- "Optimize site performance"
- "I need my site to handle more traffic"
- "Set up caching to speed up the site"

## 🎯 Specific Use Cases

### Personal Blog
```
"I want to create a cooking blog"
→ AI creates WordPress-optimized server
→ Installs blog theme
→ Configures basic SEO
→ $25/month
```

### Online Store
```
"I need an online store to sell clothes"
→ AI creates e-commerce infrastructure
→ Installs WooCommerce or Magento
→ Configures payments (PayPal, Stripe)
→ $65/month
```

### Business Website
```
"I want a professional website for my company"
→ AI creates enterprise server
→ Installs appropriate CMS
→ Configures contact forms
→ Premium SSL and advanced backup
→ $89/month
```

### Web Application
```
"I developed a React app, need to host it"
→ AI analyzes technical requirements
→ Configures Node.js environment
→ Sets up CI/CD for deployments
→ $75/month
```

## 🔒 Advanced Configuration (Optional)

### For Extra AI Features

If you want even more advanced features, also configure:

```bash
# For intelligent analysis with OpenAI
OPENAI_API_KEY="sk-your-openai-token"

# For solution comparison with Claude
ANTHROPIC_API_KEY="sk-ant-your-claude-token"

# For email alerts
ALERT_EMAIL="your-email@company.com"

# For Slack notifications
SLACK_WEBHOOK_URL="https://hooks.slack.com/..."
```

**How to get these keys:**

**OpenAI:**
1. Visit: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-`)

**Anthropic:**
1. Visit: https://console.anthropic.com/
2. Go to "API Keys" → "Create Key"  
3. Copy the key (starts with `sk-ant-`)

### Complete Configuration

```json
{
  "mcpServers": {
    "letscloud": {
      "command": "python",
      "args": ["-m", "letscloud_mcp_server"],
      "env": {
        "LETSCLOUD_API_TOKEN": "let_your-letscloud-token",
        "OPENAI_API_KEY": "sk-your-openai-token",
        "ANTHROPIC_API_KEY": "sk-ant-your-claude-token",
        "ALERT_EMAIL": "admin@yourdomain.com"
      }
    }
  }
}
```

## 🚨 Troubleshooting

### Error: "MCP server not found"
✅ **Solution:** Install the MCP server:
```bash
pip install letscloud-mcp-server
```

### Error: "Invalid API token"
✅ **Solution:** Check if you copied the complete LetsCloud token

### Error: "Connection failed" 
✅ **Solution:** Restart Claude Desktop after configuring

### AI doesn't respond about servers
✅ **Solution:** Type exactly: "List my LetsCloud servers"

### Configuration didn't work
✅ **Solution:** 
1. Check if JSON file is valid
2. Restart Claude Desktop completely
3. Test with simple command first

## 💡 Tips for Better Experience

### ✅ Works Well:
- **Be specific:** "Create a 2GB RAM WordPress server"
- **Give context:** "My store has 1000 visitors/day"
- **Ask for help:** "I don't know what server I need, help me"

### ❌ Avoid:
- Technical commands: "kubectl apply -f deployment.yaml"
- Complex jargon: "Configure the ingress controller"
- Total vagueness: "Do something"

### 🎯 Perfect Examples:
```
✅ "My WordPress site is slow for 500 visitors/day"
✅ "I need automatic backup for my online store"
✅ "I want a server that handles traffic spikes"
✅ "Help! My site went down!"
❌ "Configure nginx with load balancing"
❌ "Optimize the infrastructure"
❌ "Do something"
```

## 🎉 Ready to Start!

1. **Configure Claude Desktop** with your LetsCloud key
2. **Restart the application**
3. **Type:** "List my current servers"
4. **If it worked:** Start talking naturally!
5. **If it didn't work:** Check the configuration steps

**Suggested first conversation:**
```
"Hi! I'm new to LetsCloud MCP Server. Can you show me my current servers and help me understand how I can improve my infrastructure?"
```

From there, talk naturally about your needs! 🚀 