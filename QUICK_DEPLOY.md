# ⚡ Deploy Rápido - LetsCloud MCP Server

## 🚀 **Instalação com 1 Comando**

### **1. Criar VM no LetsCloud**
```bash
# Usando a própria AI:
"Crie uma VM Ubuntu 22.04 com 2GB RAM em São Paulo para hospedar meu servidor MCP"
```

### **2. Executar Script de Deploy**
```bash
# SSH na VM e executar:
curl -fsSL https://raw.githubusercontent.com/letscloud/letscloud-mcp-server/main/scripts/deploy.sh | bash
```

## 🎯 **O que o script faz automaticamente:**

✅ **Sistema:** Atualiza Ubuntu e instala dependências  
✅ **Python:** Configura Python 3.11 + ambiente virtual  
✅ **Projeto:** Clona repositório e instala dependências  
✅ **Configuração:** Cria arquivos .env e scripts  
✅ **Serviços:** Configura systemd + nginx + SSL  
✅ **Segurança:** Firewall + rate limiting + headers  
✅ **Monitoramento:** Health checks automáticos  

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
sudo systemctl status letscloud-mcp

# Ver logs em tempo real  
sudo journalctl -u letscloud-mcp -f

# Reiniciar serviço
sudo systemctl restart letscloud-mcp

# Testar health
curl http://localhost:8000/health

# Listar ferramentas (com API key)
curl -H "Authorization: Bearer SUA_API_KEY" http://localhost:8000/tools
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
- **Abra porta 80/443** no firewall do provedor se necessário
- **Backup regular** do arquivo `/home/mcpserver/.env`

## 🆘 **Resolução de Problemas:**

```bash
# Serviço não inicia?
sudo journalctl -u letscloud-mcp --no-pager

# Nginx com erro?
sudo nginx -t && sudo systemctl status nginx

# Python com problemas?
sudo -u mcpserver /home/mcpserver/letscloud-mcp-server/venv/bin/python -c "import letscloud_mcp_server; print('OK')"

# Redeployar completamente?
curl -fsSL https://raw.githubusercontent.com/letscloud/letscloud-mcp-server/main/scripts/deploy.sh | bash
```

---

**🎯 Deploy em 1 comando, servidor MCP online em minutos!** 