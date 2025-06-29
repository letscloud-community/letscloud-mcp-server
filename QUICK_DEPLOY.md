# ⚡ Deploy Rápido - LetsCloud MCP Server

## 🚀 **Instalação com 1 Comando**

### **1. Criar VM no LetsCloud**
```bash
# Usando a própria AI:
"Crie uma VM Ubuntu 22.04 com 2GB RAM em São Paulo para hospedar meu servidor MCP"
```

### **2. Executar Script de Deploy**
```bash
# SSH na VM e executar como root:
sudo curl -fsSL https://raw.githubusercontent.com/letscloud-community/letscloud-mcp-server/refs/heads/main/scripts/deploy_pt.sh | bash
```

**💡 Novo:** Script simplificado executa 100% como root - sem criação de usuários!

## 🎯 **O que o script faz automaticamente:**

✅ **Sistema:** Atualiza Ubuntu e instala dependências  
✅ **Python:** Detecta versão Python + ambiente virtual  
✅ **Projeto:** Clona repositório em `/opt/letscloud-mcp`  
✅ **Configuração:** Cria arquivos .env e service  
✅ **Serviços:** Configura systemd service como root  
✅ **Segurança:** Firewall + validação de credenciais  
✅ **Monitoramento:** Health checks integrados  

## 📝 **Informações Solicitadas:**

Durante a execução, você será perguntado:

1. **🔑 Token LetsCloud API** - Seu token de acesso  
2. **🔐 Chave API HTTP** - Gerada automaticamente se vazio  
3. **🌐 Porta** - Padrão: 8000  
4. **🏠 Domínio** - Opcional (usa IP se vazio)  

## 🎉 **Resultado Final:**

Após 5-10 minutos você terá:

- **🌐 Servidor HTTP:** `http://SEU_IP:8000`
- **📚 Documentação:** `http://SEU_IP:8000/docs`  
- **💊 Health Check:** `http://SEU_IP:8000/health`
- **🔐 API segura** com autenticação
- **🔄 Auto-restart** em caso de falha
- **📊 Logs** centralizados

## 🔧 **Comandos Úteis Pós-Deploy:**

```bash
# Ver status
systemctl status letscloud-mcp

# Ver logs em tempo real  
journalctl -u letscloud-mcp -f

# Reiniciar serviço
systemctl restart letscloud-mcp

# Testar health
curl http://localhost:8000/health

# Listar ferramentas (com API key)
curl -H "Authorization: Bearer SUA_API_KEY" http://localhost:8000/tools

# Ver configuração
cat /opt/letscloud-mcp/.env
```

## 🚀 **Usar com Cliente AI:**

### **Claude Desktop:**
```json
{
  "mcpServers": {
    "letscloud-remote": {
      "command": "curl",
      "args": [
        "-X", "POST", 
        "-H", "Authorization: Bearer SUA_API_KEY",
        "-H", "Content-Type: application/json",
        "http://SEU_IP:8000/tools/list_servers",
        "-d", "{\"arguments\": {}}"
      ]
    }
  }
}
```

### **HTTP Client direto:**
```python
import requests

headers = {"Authorization": "Bearer SUA_API_KEY"}
response = requests.get("http://SEU_IP:8000/tools", headers=headers)
print(response.json())
```

## ⚠️ **Notas Importantes:**

- **Salve a API Key** mostrada no final do deploy
- **Configure DNS** se usar domínio personalizado  
- **Abra porta especificada** no firewall do provedor  
- **Backup regular** do arquivo `/opt/letscloud-mcp/.env`
- **Execução como root** - configuração simplificada

## 🆘 **Resolução de Problemas:**

```bash
# Serviço não inicia?
journalctl -u letscloud-mcp --no-pager

# Verificar configuração?
cat /opt/letscloud-mcp/.env

# Python com problemas?
cd /opt/letscloud-mcp/letscloud-mcp-server && source venv/bin/activate && python -c "import letscloud_mcp_server; print('OK')"

# Redeployar completamente?
sudo curl -fsSL https://raw.githubusercontent.com/letscloud-community/letscloud-mcp-server/refs/heads/main/scripts/deploy_pt.sh | bash
```

---

**🎯 Deploy em 1 comando, servidor MCP online em minutos!** 