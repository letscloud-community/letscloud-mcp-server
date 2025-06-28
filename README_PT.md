# LetsCloud MCP Server

🤖 **Gerencie sua infraestrutura de nuvem através de conversas naturais com IA**

Um servidor [Model Context Protocol (MCP)](https://modelcontextprotocol.io) que permite gerenciar seus servidores LetsCloud simplesmente conversando com assistentes de IA como o Claude Desktop, sem necessidade de conhecimento técnico.

## 🌍 Suporte Multi-Idioma

- **🇧🇷 [README em Português](README_PT.md)** (Este documento)
- **🇺🇸 [English README](README.md)** - Complete version in English
- **📖 [Guia de Suporte de Idiomas](LANGUAGE_SUPPORT.md)** - Documentação bilíngue completa

## 🎯 O Que Você Pode Fazer

Converse naturalmente com a IA e tenha tudo resolvido:

- **"Crie um servidor para minha loja online"** → IA cria instantaneamente
- **"Meu site está lento, me ajude a corrigir"** → IA analisa e otimiza  
- **"Faça backup de todos os servidores antes da atualização"** → IA cuida de tudo
- **"Meu site caiu! Socorro!"** → IA diagnostica e recupera automaticamente

Sem programação. Sem comandos técnicos. Apenas conversa natural em **Português** ou **Inglês**.

## 🚀 Início Rápido

### **Opção 1: Instalação Local (Desktop)**

#### **1. Obtenha sua Chave da API LetsCloud**
- Visite [LetsCloud Dashboard](https://my.letscloud.io/profile/client-api)
- Ative e copie a chave da API

#### **2. Instale e Configure o Claude Desktop**
- Baixe [Claude Desktop](https://claude.ai/download)
- Adicione isto ao seu arquivo de configuração:

```json
{
  "mcpServers": {
    "letscloud": {
      "command": "python",
      "args": ["-m", "letscloud_mcp_server"],
      "env": {
        "LETSCLOUD_API_TOKEN": "seu-token-aqui"
      }
    }
  }
}
```

#### **3. Instale o Servidor MCP**
```bash
pip install git+https://github.com/letscloud/letscloud-mcp-server.git
```

### **Opção 2: Deploy Online (Recomendado para Equipes)** 🆕

#### **🌐 Deploy para Nuvem com 1 Comando**
```bash
# Crie uma VM e execute:
curl -fsSL https://raw.githubusercontent.com/letscloud/letscloud-mcp-server/main/scripts/deploy.sh | bash
```

**Resultado:** Seu servidor MCP rodando 24/7 online, acessível de qualquer lugar!

📚 **Guias Completos:**
- **📖 [Guia Completo de Deploy](DEPLOY_GUIDE.md)** - Passo a passo detalhado
- **⚡ [Guia de Deploy Rápido](QUICK_DEPLOY.md)** - Configuração com 1 comando
- **🇺🇸 [English Deploy Guide](DEPLOY_GUIDE_EN.md)** - Complete guide in English

#### **Benefícios do Deploy Online:**
- ✅ **Disponibilidade 24/7** - Funciona mesmo com seu computador desligado
- ✅ **Acesso da Equipe** - Múltiplos usuários podem usar o mesmo servidor
- ✅ **Melhor Performance** - Latência otimizada para API LetsCloud
- ✅ **Configuração Profissional** - SSL, monitoramento, auto-reinício
- ✅ **Acesso Remoto** - Use de qualquer dispositivo, em qualquer lugar

### **4. Comece a Conversar!**
Abra o Claude Desktop e diga:
```
"Oi! Me mostre meus servidores atuais e me ajude a gerenciar minha infraestrutura."
```

## 🛠️ O Que Você Pode Gerenciar

### Operações do Servidor
- Criar, iniciar, parar, reiniciar, excluir servidores
- Listar servidores e obter informações detalhadas
- Escalar recursos do servidor para cima/baixo
- Implantações multi-região

### Backup e Recuperação
- Criar snapshots para proteção de dados
- Agendamento automático de backup
- Restauração rápida de snapshots
- Procedimentos de recuperação de emergência

### Segurança e Acesso
- Gerenciamento de chaves SSH
- Manipulação de certificados SSL
- Configuração de controle de acesso
- Monitoramento de segurança

### Otimização de Custos
- Análise de uso de recursos
- Recomendações de redução de custos
- Políticas de escalonamento automático
- Monitoramento de uso e alertas

## 💬 Exemplos de Conversas

### Usuário Iniciante
```
Você: "Preciso de um site para meu pequeno negócio"
IA: "Vou te ajudar a criar um site profissional. Que tipo de negócio?"
Você: "É uma padaria, quero mostrar meus produtos e receber pedidos"
IA: "Perfeito! Criando um site de padaria com pedidos online..."
✅ Site WordPress criado com e-commerce
✅ Processamento de pagamento configurado  
✅ Segurança SSL habilitada
✅ Pronto em 10 minutos - R$ 35/mês
```

### Resposta de Emergência
```
Você: "SOCORRO! Meu site caiu durante nossa maior promoção!"
IA: "🚨 Emergência detectada! Investigando imediatamente..."
🔍 Diagnosticado: Sobrecarga do servidor por alto tráfego
⚡ Criando servidor de emergência com 3x a capacidade
✅ Site restaurado em 8 minutos com auto-escalonamento
```

## 🌟 Por Que Escolher o LetsCloud MCP Server?

✅ **Zero Conhecimento Técnico Necessário** - Apenas converse naturalmente  
✅ **Funciona em Inglês e Português** - Suporte nativo aos idiomas  
✅ **Resposta Instantânea a Emergências** - IA lida com crises automaticamente  
✅ **Otimização de Custos** - IA encontra oportunidades de economia  
✅ **Monitoramento 24/7** - Prevenção proativa de problemas  
✅ **Arquitetura Escalável** - Cresce com seu negócio  
✅ **Segurança Empresarial** - Proteção de dados nível bancário  
✅ **Deploy Online** - Acesso remoto de qualquer lugar 🆕

## 🤖 Plataformas de IA Suportadas

- **✅ Claude Desktop** (Recomendado - Melhor experiência)
- **✅ Cline** (Extensão VS Code)  
- **✅ Zed Editor**
- **⏳ ChatGPT** (Em breve na GPT Store)
- **✅ Qualquer cliente compatível com MCP**
- **🆕 API HTTP/WebSocket** - Acesso remoto via API REST

## 🔧 Opções de Instalação

### **Instalação Local**
```bash
# Opção A: Instalar do GitHub (Recomendado)
pip install git+https://github.com/letscloud/letscloud-mcp-server.git

# Opção B: Instalar do Código Fonte  
git clone https://github.com/letscloud/letscloud-mcp-server.git
cd letscloud-mcp-server
pip install -e .

# Opção C: Instalar do PyPI (Em Breve)
pip install letscloud-mcp-server
```

### **Deploy Online** 🆕
```bash
# Deploy na nuvem com um comando
curl -fsSL https://raw.githubusercontent.com/letscloud/letscloud-mcp-server/main/scripts/deploy.sh | bash
```

**📚 Documentação Completa de Deploy:**
- **🇧🇷 [Guia de Deploy em Português](DEPLOY_GUIDE.md)** - Passo a passo completo
- **🇺🇸 [English Deploy Guide](DEPLOY_GUIDE_EN.md)** - Complete step-by-step
- **⚡ [Deploy Rápido (PT)](QUICK_DEPLOY.md)** - Configuração com 1 comando
- **⚡ [Quick Deploy (EN)](QUICK_DEPLOY_EN.md)** - One-command setup

## 🌍 Suporte de Idiomas

Este projeto fornece documentação e suporte completos em:
- **Português** - Para usuários brasileiros
- **English** - For international users

Os assistentes de IA detectarão automaticamente seu idioma e responderão adequadamente, adaptando:
- Moeda (BRL vs USD)
- Métodos de pagamento (PIX vs Cartões de crédito)
- Conformidade legal (LGPD vs GDPR)
- Contextos de negócios (Mercado brasileiro vs Global)

**🇺🇸 For international users:** Access the [complete documentation in English](README.md).

## 🚀 Modos de Deploy

### **🏠 Modo Local**
- **Melhor para:** Desenvolvedores individuais, testes, desenvolvimento
- **Instalação:** Simples pip install
- **Requisitos:** Ambiente Python local
- **Acesso:** Apenas computador local

### **🌐 Modo Online** 🆕  
- **Melhor para:** Equipes, produção, disponibilidade 24/7
- **Instalação:** Deploy na nuvem com um comando
- **Requisitos:** VM/VPS com Ubuntu
- **Acesso:** De qualquer lugar via API HTTP/WebSocket
- **Recursos:** SSL, monitoramento, auto-reinício, acesso de equipe

## 📞 Suporte e Comunidade

- **🐛 Reportar Bugs**: [GitHub Issues](https://github.com/letscloud/letscloud-mcp-server/issues)
- **💬 Perguntas**: [GitHub Discussions](https://github.com/letscloud/letscloud-mcp-server/discussions)
- **🌐 Suporte LetsCloud**: [support@letscloud.io](mailto:support@letscloud.io)
- **🌍 Multi-idioma**: Suporte disponível em inglês e português

## 🤝 Contribuindo

Damos as boas-vindas a contribuições! Por favor, veja nosso [Guia de Contribuição](CONTRIBUTING.md) para detalhes.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- [Model Context Protocol](https://modelcontextprotocol.io) pela Anthropic
- [LetsCloud](https://letscloud.io) pela API de infraestrutura
- A comunidade open source pela inspiração e suporte