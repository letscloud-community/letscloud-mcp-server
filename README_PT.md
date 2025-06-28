# LetsCloud MCP Server

🤖 **Gerencie sua infraestrutura em nuvem através de conversas naturais com IA**

Um servidor [Model Context Protocol (MCP)](https://modelcontextprotocol.io) que permite gerenciar seus servidores LetsCloud simplesmente conversando com assistentes de IA como Claude Desktop, sem precisar de conhecimento técnico.

## 🎯 O que Você Pode Fazer

Converse naturalmente com IA e faça tudo acontecer:

- **"Crie um servidor para minha loja online"** → IA cria instantaneamente
- **"Meu site está lento, ajude a resolver"** → IA analisa e otimiza  
- **"Faça backup de todos os servidores antes da atualização"** → IA cuida de tudo
- **"Meu site caiu! Socorro!"** → IA diagnostica e recupera automaticamente

Sem programação. Sem comandos técnicos. Apenas conversa natural em português ou inglês.

## 🚀 Início Rápido

### 1. Obtenha sua Chave API LetsCloud
- Acesse [Painel LetsCloud](https://my.letscloud.io/profile/client-api)
- Habilite e copie a chave API

### 2. Instale e Configure Claude Desktop
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

### 3. Instale o Servidor MCP
```bash
pip install git+https://github.com/letscloud/letscloud-mcp-server.git
```

### 4. Comece a Conversar!
Abra Claude Desktop e diga:
```
"Oi! Mostre meus servidores atuais e me ajude a gerenciar minha infraestrutura."
```

## 🛠️ O que Você Pode Gerenciar

### Operações de Servidor
- Criar, iniciar, parar, reiniciar, deletar servidores
- Listar servidores e obter informações detalhadas
- Escalar recursos para cima/baixo
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
Você: "É uma padaria, quero mostrar produtos e receber pedidos"
IA: "Perfeito! Criando um site de padaria com pedidos online..."
✅ Site WordPress criado com e-commerce
✅ Processamento de pagamento configurado  
✅ Segurança SSL habilitada
✅ Pronto em 10 minutos - R$ 65/mês
```

### Resposta de Emergência
```
Você: "SOCORRO! Meu site saiu do ar durante nossa maior promoção!"
IA: "🚨 Emergência detectada! Investigando imediatamente..."
🔍 Diagnosticado: Sobrecarga do servidor por alto tráfego
⚡ Criando servidor emergencial com 3x a capacidade
✅ Site restaurado em 8 minutos com auto-escalonamento
```

## 🌟 Por que Escolher LetsCloud MCP Server?

✅ **Zero Conhecimento Técnico Necessário** - Apenas converse naturalmente  
✅ **Funciona em Português e Inglês** - Suporte nativo ao idioma  
✅ **Resposta Emergencial Instantânea** - IA lida com crises automaticamente  
✅ **Otimização de Custos** - IA encontra oportunidades de economia  
✅ **Monitoramento 24/7** - Prevenção proativa de problemas  
✅ **Arquitetura Escalável** - Cresce com seu negócio  
✅ **Segurança Empresarial** - Proteção de dados nível bancário  

## 🤖 Plataformas de IA Suportadas

- **✅ Claude Desktop** (Recomendado - Melhor experiência)
- **✅ Cline** (extensão VS Code)  
- **✅ Zed Editor**
- **⏳ ChatGPT** (Em breve na GPT Store)
- **✅ Qualquer cliente compatível com MCP**

## 🔧 Instalação

### Pré-requisitos
- Python 3.11+
- Conta LetsCloud com acesso à API
- Cliente de IA compatível com MCP

### Opção A: Instalar do GitHub (Recomendado)
```bash
pip install git+https://github.com/letscloud/letscloud-mcp-server.git
```

### Opção B: Instalar do Código Fonte
```bash
git clone https://github.com/letscloud/letscloud-mcp-server.git
cd letscloud-mcp-server
pip install -e .
```

### Opção C: Instalar do PyPI (Em Breve)
```bash
# Estará disponível após publicação no PyPI
pip install letscloud-mcp-server
```

## 🌍 Suporte Multi-idioma

Este projeto fornece documentação completa em:
- **Português** - Para usuários brasileiros
- **English** - For international users

Todos os exemplos de conversas e guias estão disponíveis em ambos os idiomas.

## 📞 Suporte e Comunidade

- **🐛 Relatórios de Bug**: [GitHub Issues](https://github.com/letscloud/letscloud-mcp-server/issues)
- **💬 Perguntas**: [GitHub Discussions](https://github.com/letscloud/letscloud-mcp-server/discussions)
- **🌐 Suporte LetsCloud**: [support@letscloud.io](mailto:support@letscloud.io)

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.