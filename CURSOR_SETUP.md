# 🎯 Configuração do Cursor para LetsCloud MCP

## 📋 Pré-requisitos

✅ **LetsCloud MCP Server** instalado e funcionando
✅ **Token da API LetsCloud** configurado
✅ **Cursor/Claude Desktop** instalado

---

## 🔧 Configuração do Cursor

### 1. Localizar o Arquivo de Configuração

O Cursor/Claude Desktop usa um arquivo de configuração JSON. Localize o arquivo correto:

**Linux/WSL:**
```bash
~/.config/Claude/claude_desktop_config.json
```

**macOS:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```bash
%APPDATA%/Claude/claude_desktop_config.json
```

### 2. Criar/Editar o Arquivo de Configuração

Se o arquivo não existir, crie-o. Se existir, adicione nosso servidor à seção `mcpServers`:

```json
{
  "mcpServers": {
    "letscloud": {
      "command": "python",
      "args": [
        "-m",
        "letscloud_mcp_server"
      ],
      "cwd": "/home/marcio/letscloud-mcp",
      "env": {
        "LETSCLOUD_API_TOKEN": "$2Y$10$EWJTQ6EHOTBRQYVUUFEKWP6D4SVUTVVCFRBXSSREVGMPPPU"
      }
    }
  }
}
```

### 3. Ajustar o Caminho

**⚠️ IMPORTANTE**: Altere o `"cwd"` para o caminho correto do seu projeto:

```bash
# No WSL/Linux
"cwd": "/home/marcio/letscloud-mcp"

# No Windows
"cwd": "C:\\Users\\SEU_USUARIO\\letscloud-mcp"

# No macOS  
"cwd": "/Users/SEU_USUARIO/letscloud-mcp"
```

---

## 🚀 Ativação do MCP

### 1. Reiniciar o Cursor/Claude Desktop

Feche completamente e reabra o aplicativo.

### 2. Verificar Conexão

No chat, você deve ver:
- 🔌 **Ícone de conexão MCP** na interface
- 📋 **20 ferramentas LetsCloud** disponíveis

### 3. Testar Comandos

```
@letscloud list my instances
@letscloud list locations  
@letscloud get account info
```

---

## 🛠️ Ferramentas Disponíveis (20 Total)

### 🖥️ **Gerenciamento de Instâncias (7)**
- `list_servers` - Listar todas as instâncias
- `get_server` - Obter detalhes de uma instância  
- `create_server` - Criar nova instância
- `delete_server` - Deletar instância
- `reboot_server` - Reiniciar instância
- `shutdown_server` - Desligar instância  
- `start_server` - Iniciar instância

### 🔑 **Gerenciamento SSH (4)**
- `list_ssh_keys` - Listar chaves SSH
- `get_ssh_key` - Obter detalhes de chave SSH
- `create_ssh_key` - Criar nova chave SSH
- `delete_ssh_key` - Deletar chave SSH

### 📸 **Gerenciamento Snapshots (5)**
- `list_snapshots` - Listar snapshots
- `get_snapshot` - Obter detalhes de snapshot
- `create_snapshot` - Criar snapshot
- `delete_snapshot` - Deletar snapshot
- `restore_snapshot` - Restaurar snapshot

### 📋 **Recursos e Informações (4)**
- `list_plans` - Listar planos disponíveis
- `list_images` - Listar imagens de SO
- `list_locations` - Listar localizações
- `get_account_info` - Informações da conta

---

## 💬 Exemplos de Uso

### Gerenciamento Básico
```
"Liste minhas instâncias LetsCloud"
"Crie uma nova instância Ubuntu em São Paulo"
"Reinicie a instância com ID 123"
"Mostre informações da minha conta"
```

### Gerenciamento Avançado
```
"Crie um snapshot da instância blog-br"
"Liste todas as localizações disponíveis"
"Adicione uma nova chave SSH chamada 'laptop'"
"Quais planos estão disponíveis?"
```

### Bilíngue (Português/Inglês)
```
"Show my LetsCloud instances"
"Create a snapshot of my server"
"Mostre os planos disponíveis"
"List all SSH keys"
```

---

## 🔍 Troubleshooting

### ❌ **Servidor não conecta**
- Verifique se o caminho `cwd` está correto
- Confirme que o token `LETSCLOUD_API_TOKEN` é válido
- Teste o servidor manualmente: `python -m letscloud_mcp_server --version`

### ❌ **Ferramentas não aparecem**
- Reinicie o Cursor/Claude Desktop
- Verifique a sintaxe JSON da configuração
- Confirme que está usando a versão mais recente do Cursor

### ❌ **Erro de API**
- Verifique se a API está ativada em [my.letscloud.io](https://my.letscloud.io)
- Confirme que o token não expirou
- Teste a conexão: `curl -H "api-token: SEU_TOKEN" https://core.letscloud.io/api/profile`

---

## ✅ Status da Configuração

**🎯 Servidor MCP**: `letscloud-mcp-server 1.0.0`
**🔑 Autenticação**: Header `api-token` configurado
**🌐 API**: `https://core.letscloud.io/api`
**📦 Compatibilidade**: MCP v1.10.1
**🛠️ Ferramentas**: 20 tools completas

---

## 🎉 Pronto!

Agora você pode gerenciar sua infraestrutura LetsCloud diretamente através de conversas naturais no Cursor/Claude Desktop!

**Comandos populares para começar:**
- `@letscloud list my instances`
- `@letscloud show account info`
- `@letscloud list available locations` 