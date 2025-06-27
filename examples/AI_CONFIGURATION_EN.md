# LetsCloud MCP Server Configuration on AI Platforms

Complete configuration guide for using the LetsCloud MCP Server with different AI assistants.

## 🎯 Prerequisites

Before configuring any AI platform, you need:

1. **Active LetsCloud account**
   - Visit: https://cloud.letscloud.io
   - Create your free account

2. **LetsCloud API token**
   - Log into your LetsCloud account
   - Go to "Settings" → "API" 
   - Click "Generate New Key"
   - Copy the token (starts with `let_`)

3. **Python 3.11+ installed**
   - Windows: https://python.org/downloads
   - Mac: `brew install python3`
   - Linux: `sudo apt install python3 python3-pip`

4. **LetsCloud MCP Server installed**
   ```bash
   pip install letscloud-mcp-server
   ```

## 🖥️ Claude Desktop (Recommended)

### Why Claude Desktop?
- ✅ Simplest configuration
- ✅ User-friendly interface
- ✅ Native MCP support
- ✅ Works perfectly with natural conversation

### Step-by-Step Installation

#### 1. Install Claude Desktop
- **Download:** https://claude.ai/download
- **Versions:** Windows, Mac, Linux
- **Create account:** Free or Claude Pro

#### 2. Locate Configuration File

**Windows:**
```
C:\Users\[your-username]\AppData\Roaming\Claude\claude_desktop_config.json
```
Or type in Windows + R:
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Mac:**
```
/Users/[your-username]/Library/Application Support/Claude/claude_desktop_config.json
```
Or in Terminal:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```
/home/[your-username]/.config/claude/claude_desktop_config.json
```
Or:
```
~/.config/claude/claude_desktop_config.json
```

#### 3. Configure the MCP Server

Open the configuration file and add:

```json
{
  "mcpServers": {
    "letscloud": {
      "command": "python",
      "args": ["-m", "letscloud_mcp_server"],
      "env": {
        "LETSCLOUD_API_TOKEN": "let_YOUR_TOKEN_HERE"
      }
    }
  }
}
```

**⚠️ Important:**
- Replace `let_YOUR_TOKEN_HERE` with your actual token
- Keep the quotes around the token
- Save the file

#### 4. Advanced Configuration (Optional)

For extra features like OpenAI/Anthropic integration:

```json
{
  "mcpServers": {
    "letscloud": {
      "command": "python",
      "args": ["-m", "letscloud_mcp_server"],
      "env": {
        "LETSCLOUD_API_TOKEN": "let_your_letscloud_token",
        "OPENAI_API_KEY": "sk_your_openai_token",
        "ANTHROPIC_API_KEY": "sk-ant_your_anthropic_token",
        "ALERT_EMAIL": "your@email.com"
      }
    }
  }
}
```

#### 5. Test Configuration

1. **Close Claude Desktop completely**
2. **Open Claude Desktop again**
3. **Type:** "List my LetsCloud servers"
4. **If it worked:** You'll see your servers list! 🎉
5. **If it didn't work:** See "Troubleshooting" section

## 🤖 Cline (VS Code)

### For Developers

If you use VS Code, you can use Cline:

#### 1. Install Cline Extension
- Open VS Code
- Go to Extensions (Ctrl+Shift+X)
- Search for "Cline"
- Install the extension

#### 2. Configure MCP
- Open Command Palette (Ctrl+Shift+P)
- Type "Cline: Configure MCP"
- Add configuration:

```json
{
  "mcpServers": {
    "letscloud": {
      "command": "python",
      "args": ["-m", "letscloud_mcp_server"],
      "env": {
        "LETSCLOUD_API_TOKEN": "let_your_token_here"
      }
    }
  }
}
```

#### 3. Use
- Open Cline chat
- Type: "Show my LetsCloud servers"

## 📱 Other MCP Clients

### Zed Editor
```json
{
  "assistant": {
    "mcp_servers": {
      "letscloud": {
        "command": "python",
        "args": ["-m", "letscloud_mcp_server"],
        "env": {
          "LETSCLOUD_API_TOKEN": "let_your_token"
        }
      }
    }
  }
}
```

### Continue (VS Code)
Similar to Cline, but configuration in:
```
.continue/config.json
```

## 🚫 OpenAI ChatGPT - Coming Soon

### Current Status
- ❌ ChatGPT Web doesn't support MCP yet
- ❌ GPT Store doesn't accept MCP servers yet
- ⏳ OpenAI is working on MCP support

### For Enterprises
If your company has an Enterprise contract with OpenAI:
- Contact your account manager
- Request custom MCP integration
- They can implement via API

### Temporary Alternative
Use Claude Desktop - it has the same conversation quality!

## 🔧 Advanced Configurations

### Extra API Tokens

#### OpenAI (For intelligent analysis)
1. Visit: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Name it: "LetsCloud MCP"
4. Copy the key (starts with `sk-`)

#### Anthropic (For comparisons)
1. Visit: https://console.anthropic.com/
2. Go to "API Keys"
3. Click "Create Key"
4. Copy the key (starts with `sk-ant-`)

### Complete Configuration
```json
{
  "mcpServers": {
    "letscloud": {
      "command": "python",
      "args": ["-m", "letscloud_mcp_server"],
      "env": {
        "LETSCLOUD_API_TOKEN": "let_required",
        "OPENAI_API_KEY": "sk-optional_for_analysis",
        "ANTHROPIC_API_KEY": "sk-ant-optional_comparisons",
        "ALERT_EMAIL": "optional@email.com",
        "SLACK_WEBHOOK_URL": "https://hooks.slack.com/optional"
      }
    }
  }
}
```

## 🚨 Troubleshooting

### Error: "MCP server not found"

**Cause:** MCP Server not installed  
**Solution:**
```bash
pip install letscloud-mcp-server
```

### Error: "Invalid API token"

**Cause:** Incorrect LetsCloud token  
**Solutions:**
1. Check if you copied the complete token
2. Generate new token on LetsCloud
3. Check for extra spaces

### Error: "Connection failed"

**Cause:** Incorrect configuration  
**Solutions:**
1. Restart Claude Desktop completely
2. Check if JSON file is valid
3. Use online JSON validator

### AI doesn't respond about servers

**Solutions:**
1. Type exactly: "List my LetsCloud servers"
2. Try: "What LetsCloud tools are available?"
3. Restart AI after configuring

### Configuration file doesn't exist

**Solutions:**
1. **Windows:** Create folder `%APPDATA%\Claude\`
2. **Mac/Linux:** Create folder `~/.config/claude/`
3. Create file `claude_desktop_config.json`
4. Paste basic configuration

### Python not found

**Solutions:**
1. Install Python: https://python.org/downloads
2. Add Python to PATH
3. Test: `python --version`
4. If it doesn't work, try: `python3 -m letscloud_mcp_server`

## ✅ Testing if It Worked

### Test Commands
```
1. "List my LetsCloud servers"
2. "What server plans are available?"
3. "Show my SSH keys"
4. "What's my LetsCloud account status?"
```

### Expected Response
AI should respond with real information from your LetsCloud account.

### If It Didn't Work
1. ❌ Wrong token → Generate new token
2. ❌ Wrong configuration → Review JSON
3. ❌ Python not installed → Install Python
4. ❌ MCP not installed → `pip install letscloud-mcp-server`

## 🎉 First Conversation

After configuring, start with:

```
"Hi! I just configured the LetsCloud MCP Server. 
Can you show me my current servers and explain 
how I can manage my infrastructure through AI?"
```

From there, talk naturally! 🚀

## 📞 Support

### If you need help:
- **Technical configuration:** This document
- **LetsCloud issues:** LetsCloud support
- **Claude issues:** Anthropic support  
- **MCP Server bugs:** GitHub Issues

### Additional Documentation:
- [MCP Protocol](https://modelcontextprotocol.io)
- [LetsCloud API](https://api.letscloud.io/docs)
- [Claude Desktop](https://claude.ai/download) 