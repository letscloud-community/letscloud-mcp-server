# Configuração do LetsCloud MCP Server em Plataformas de IA

Guia completo de configuração para usar o LetsCloud MCP Server com diferentes assistentes de IA.

## 🎯 Pré-requisitos

Antes de configurar qualquer plataforma de IA, você precisa:

1. **Conta LetsCloud ativa**
   - Acesse: https://cloud.letscloud.io
   - Crie sua conta gratuita

2. **Token de API LetsCloud**
   - Entre na sua conta LetsCloud
   - Vá em "Configurações" → "API" 
   - Clique "Gerar Nova Chave"
   - Copie o token (começa com `let_`)

3. **Python 3.11+ instalado**
   - Windows: https://python.org/downloads
   - Mac: `brew install python3`
   - Linux: `sudo apt install python3 python3-pip`

4. **LetsCloud MCP Server instalado**
   ```bash
   pip install letscloud-mcp-server
   ```

## 🖥️ Claude Desktop (Recomendado)

### Por que Claude Desktop?
- ✅ Configuração mais simples
- ✅ Interface amigável
- ✅ Suporte nativo ao MCP
- ✅ Funciona perfeitamente com conversação natural

### Instalação Passo a Passo

#### 1. Instalar Claude Desktop
- **Download:** https://claude.ai/download
- **Versões:** Windows, Mac, Linux
- **Criar conta:** Gratuita ou Claude Pro

#### 2. Localizar Arquivo de Configuração

**Windows:**
```
C:\Users\[seu-usuario]\AppData\Roaming\Claude\claude_desktop_config.json
```
Ou digite no Windows + R:
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Mac:**
```
/Users/[seu-usuario]/Library/Application Support/Claude/claude_desktop_config.json
```
Ou no Terminal:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```
/home/[seu-usuario]/.config/claude/claude_desktop_config.json
```
Ou:
```
~/.config/claude/claude_desktop_config.json
```

#### 3. Configurar o MCP Server

Abra o arquivo de configuração e adicione:

```json
{
  "mcpServers": {
    "letscloud": {
      "command": "python",
      "args": ["-m", "letscloud_mcp_server"],
      "env": {
        "LETSCLOUD_API_TOKEN": "let_SEU_TOKEN_AQUI"
      }
    }
  }
}
```

**⚠️ Importante:**
- Substitua `let_SEU_TOKEN_AQUI` pelo seu token real
- Mantenha as aspas no token
- Salve o arquivo

#### 4. Configuração Avançada (Opcional)

Para recursos extras como integração com OpenAI/Anthropic:

```json
{
  "mcpServers": {
    "letscloud": {
      "command": "python",
      "args": ["-m", "letscloud_mcp_server"],
      "env": {
        "LETSCLOUD_API_TOKEN": "let_seu_token_letscloud",
        "OPENAI_API_KEY": "sk_seu_token_openai",
        "ANTHROPIC_API_KEY": "sk-ant_seu_token_anthropic",
        "ALERT_EMAIL": "seu@email.com"
      }
    }
  }
}
```

#### 5. Testar Configuração

1. **Feche Claude Desktop completamente**
2. **Abra Claude Desktop novamente**
3. **Digite:** "Liste meus servidores LetsCloud"
4. **Se funcionou:** Verá lista dos seus servidores! 🎉
5. **Se não funcionou:** Veja seção "Resolução de Problemas"

## 🤖 Cline (VS Code)

### Para Desenvolvedores

Se você usa VS Code, pode usar o Cline:

#### 1. Instalar Extensão Cline
- Abra VS Code
- Vá em Extensions (Ctrl+Shift+X)
- Procure "Cline"
- Instale a extensão

#### 2. Configurar MCP
- Abra Command Palette (Ctrl+Shift+P)
- Digite "Cline: Configure MCP"
- Adicione configuração:

```json
{
  "mcpServers": {
    "letscloud": {
      "command": "python",
      "args": ["-m", "letscloud_mcp_server"],
      "env": {
        "LETSCLOUD_API_TOKEN": "let_seu_token_aqui"
      }
    }
  }
}
```

#### 3. Usar
- Abra chat do Cline
- Digite: "Mostre meus servidores LetsCloud"

## 📱 Outros Clientes MCP

### Zed Editor
```json
{
  "assistant": {
    "mcp_servers": {
      "letscloud": {
        "command": "python",
        "args": ["-m", "letscloud_mcp_server"],
        "env": {
          "LETSCLOUD_API_TOKEN": "let_seu_token"
        }
      }
    }
  }
}
```

### Continue (VS Code)
Similar ao Cline, mas configuração em:
```
.continue/config.json
```

## 🚫 OpenAI ChatGPT - Em Breve

### Status Atual
- ❌ ChatGPT Web não suporta MCP ainda
- ❌ GPT Store não aceita MCP servers ainda
- ⏳ OpenAI está trabalhando no suporte

### Para Empresas
Se sua empresa tem contrato Enterprise com OpenAI:
- Contate seu gerente de conta
- Solicite integração MCP custom
- Eles podem implementar via API

### Alternativa Temporária
Use Claude Desktop - tem a mesma qualidade de conversação!

## 🔧 Configurações Avançadas

### Tokens de API Extras

#### OpenAI (Para análises inteligentes)
1. Acesse: https://platform.openai.com/api-keys
2. Clique "Create new secret key"
3. Nomeie: "LetsCloud MCP"
4. Copie a chave (começa com `sk-`)

#### Anthropic (Para comparações)
1. Acesse: https://console.anthropic.com/
2. Vá em "API Keys"
3. Clique "Create Key"
4. Copie a chave (começa com `sk-ant-`)

### Configuração Completa
```json
{
  "mcpServers": {
    "letscloud": {
      "command": "python",
      "args": ["-m", "letscloud_mcp_server"],
      "env": {
        "LETSCLOUD_API_TOKEN": "let_obrigatorio",
        "OPENAI_API_KEY": "sk-opcional_para_analises",
        "ANTHROPIC_API_KEY": "sk-ant-opcional_comparacoes",
        "ALERT_EMAIL": "opcional@email.com",
        "SLACK_WEBHOOK_URL": "https://hooks.slack.com/opcional"
      }
    }
  }
}
```

## 🚨 Resolução de Problemas

### Erro: "MCP server not found"

**Causa:** MCP Server não está instalado  
**Solução:**
```bash
pip install letscloud-mcp-server
```

### Erro: "Invalid API token"

**Causa:** Token LetsCloud incorreto  
**Soluções:**
1. Verifique se copiou o token completo
2. Gere novo token na LetsCloud
3. Verifique se não há espaços extras

### Erro: "Connection failed"

**Causa:** Configuração incorreta  
**Soluções:**
1. Reinicie Claude Desktop completamente
2. Verifique se arquivo JSON está válido
3. Use validador JSON online

### IA não responde sobre servidores

**Soluções:**
1. Digite exatamente: "Liste meus servidores LetsCloud"
2. Tente: "Que ferramentas do LetsCloud estão disponíveis?"
3. Reinicie a IA após configurar

### Arquivo de configuração não existe

**Soluções:**
1. **Windows:** Crie a pasta `%APPDATA%\Claude\`
2. **Mac/Linux:** Crie a pasta `~/.config/claude/`
3. Crie o arquivo `claude_desktop_config.json`
4. Cole a configuração básica

### Python não encontrado

**Soluções:**
1. Instale Python: https://python.org/downloads
2. Adicione Python ao PATH
3. Teste: `python --version`
4. Se não funcionar, tente: `python3 -m letscloud_mcp_server`

## ✅ Testando se Funcionou

### Comandos de Teste
```
1. "Liste meus servidores LetsCloud"
2. "Que planos de servidor estão disponíveis?"
3. "Mostre minhas chaves SSH"
4. "Qual é o status da minha conta LetsCloud?"
```

### Resposta Esperada
A IA deve responder com informações reais da sua conta LetsCloud.

### Se Não Funcionou
1. ❌ Token incorreto → Gere novo token
2. ❌ Configuração errada → Revise JSON
3. ❌ Python não instalado → Instale Python
4. ❌ MCP não instalado → `pip install letscloud-mcp-server`

## 🎉 Primeira Conversa

Depois que configurar, comece com:

```
"Oi! Acabei de configurar o LetsCloud MCP Server. 
Pode me mostrar meus servidores atuais e me explicar 
como posso gerenciar minha infraestrutura através de IA?"
```

A partir daí, converse naturalmente! 🚀

## 📞 Suporte

### Se precisar de ajuda:
- **Configuração técnica:** Este documento
- **Problemas com LetsCloud:** Suporte LetsCloud
- **Problemas com Claude:** Suporte Anthropic  
- **Bugs do MCP Server:** GitHub Issues

### Documentação Adicional:
- [MCP Protocol](https://modelcontextprotocol.io)
- [LetsCloud API](https://api.letscloud.io/docs)
- [Claude Desktop](https://claude.ai/download) 