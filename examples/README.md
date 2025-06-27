# LetsCloud MCP Server - Guia do Usuário

Este guia mostra como usar o LetsCloud MCP Server através de interfaces de IA como Claude Desktop, ChatGPT e outros assistentes inteligentes para gerenciar sua infraestrutura em linguagem natural.

## 🤖 O que é possível fazer?

Com o LetsCloud MCP Server integrado à sua IA, você pode:

- **"Crie um servidor para minha loja online"** → IA cria automaticamente
- **"Meu site está lento, o que fazer?"** → IA analisa e otimiza
- **"Faça backup de tudo antes da atualização"** → IA executa backup completo
- **"Preciso que meu site aguente mais visitantes"** → IA escala a infraestrutura
- **"Meu site saiu do ar, socorro!"** → IA diagnostica e resolve emergências

## 🔧 Configuração por Plataforma

### Claude Desktop (Recomendado)

1. **Obter sua API Key LetsCloud**
   ```
   Acesse: https://cloud.letscloud.io/account/api
   Copie seu token: let_1234567890abcdef...
   ```

2. **Configurar Claude Desktop**
   ```json
   {
     "mcpServers": {
       "letscloud": {
         "command": "python",
         "args": ["-m", "letscloud_mcp_server"],
         "env": {
           "LETSCLOUD_API_TOKEN": "let_seu-token-aqui"
         }
       }
     }
   }
   ```

3. **Localização do arquivo de configuração:**
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/claude/claude_desktop_config.json`

4. **Reiniciar Claude Desktop** após salvar a configuração

### OpenAI ChatGPT (GPT Store)

1. **Aguardando aprovação** - Em breve disponível na GPT Store
2. **Versão Enterprise**: Contate suporte para integração custom

### Outros Assistentes IA

O MCP Server funciona com qualquer IA que suporte o protocolo MCP:
- **Cline** (VS Code)
- **Zed Editor**
- **Outros clientes MCP**

## 💬 Como Usar - Exemplos de Conversas

### Cenário 1: Cliente Iniciante

**Você:** "Oi! Preciso de um servidor para meu blog WordPress"

**IA:** "Claro! Vou criar um servidor otimizado para WordPress. Algumas perguntas rápidas:
- Quantos visitantes por mês você espera?
- Já tem domínio registrado?
- Quer instalação automática do WordPress?"

**Você:** "Uns 500 visitantes, já tenho domínio, sim quero automático"

**IA:** "Perfeito! Criando agora:
✅ Servidor criado: 2GB RAM, Ubuntu 22.04
✅ WordPress instalado e configurado  
✅ SSL gratuito ativado
✅ Backup diário configurado
💰 Custo: R$ 35/mês
🌐 IP: 165.232.123.45
⏱️ Pronto em 5 minutos!"

### Cenário 2: E-commerce em Crescimento

**Você:** "Minha loja virtual está ficando lenta, tenho 1000 visitantes por dia agora"

**IA:** "Identifico que você precisa escalar! Seu crescimento é ótimo. Vou implementar:

🏗️ **Nova Arquitetura:**
- Load Balancer para distribuir tráfego
- 2 servidores web para redundância  
- Servidor de banco dedicado
- Sistema de cache para velocidade

💰 **Custo:** R$ 89/mês (vs R$ 45 atual)
🚀 **Benefício:** Suporta até 10.000 visitantes/dia
⚡ **Velocidade:** 3x mais rápido
🛡️ **Disponibilidade:** 99.9%

Quer que eu implemente agora?"

### Cenário 3: Emergência

**Você:** "SOCORRO! Meu site saiu do ar há 20 minutos!"

**IA:** "🚨 **EMERGÊNCIA DETECTADA** - Iniciando diagnóstico imediato...

🔍 **Diagnóstico:**
- Servidor principal não responde ❌
- Problema: Falha de hardware
- Backup disponível: 2 horas atrás ✅

⚡ **Recuperação em andamento:**
- 00:00 Criando servidor emergencial
- 00:03 Restaurando backup  
- 00:07 Redirecionando DNS
- 00:09 ✅ SITE FUNCIONANDO!

**Total:** 9 minutos de indisponibilidade
**Prevenção:** Configurei alta disponibilidade para evitar futuras falhas"

## 🎯 Casos de Uso por Tipo de Negócio

### 🍕 Restaurante - Delivery
**Você:** "Preciso de um site para delivery do meu restaurante"
**IA cria:** Site com cardápio, pedidos online, integração WhatsApp, pagamento PIX

### 🎓 Escola Online  
**Você:** "Quero uma plataforma de cursos online"
**IA cria:** Moodle configurado, área do aluno, upload de vídeos, certificados

### ⚖️ Escritório de Advocacia
**Você:** "Preciso de um site profissional para meu escritório"
**IA cria:** Site institucional, área do cliente, upload seguro, conformidade LGPD

### 📸 Fotógrafo
**Você:** "Quero mostrar meu portfólio e vender fotos"
**IA cria:** Galeria profissional, proteção de imagens, e-commerce integrado

## 🔒 Configuração Segura

### Variáveis de Ambiente (Opcional)

Para recursos avançados, configure:

```bash
# Obrigatório
LETSCLOUD_API_TOKEN="let_seu-token-aqui"

# Opcional - Para recursos de IA aprimorados
OPENAI_API_KEY="sk-seu-token-openai"      # Para análises inteligentes
ANTHROPIC_API_KEY="sk-ant-seu-token"      # Para comparação de recomendações

# Opcional - Para alertas
ALERT_EMAIL="admin@seudominio.com"        # Receber alertas por email
SLACK_WEBHOOK_URL="https://hooks.slack..."# Notificações no Slack
```

### Obtendo as Chaves

**LetsCloud API (Obrigatório):**
1. Acesse https://cloud.letscloud.io/account/api
2. Clique em "Gerar Nova Chave"
3. Copie o token que começa com `let_`

**OpenAI (Opcional):**
1. Acesse https://platform.openai.com/api-keys
2. Clique "Create new secret key"
3. Copie a chave que começa com `sk-`

**Anthropic Claude (Opcional):**
1. Acesse https://console.anthropic.com/
2. Vá em "API Keys" → "Create Key"
3. Copie a chave que começa com `sk-ant-`

## 💡 Recursos Inteligentes

### Com OpenAI Integration
- **Análise de logs inteligente:** "Por que meu site está lento hoje?"
- **Otimização automática:** "Reduza meus custos sem perder performance"
- **Planejamento de arquitetura:** "Preciso suportar 50.000 usuários"

### Com Claude Integration  
- **Comparação de soluções:** Recebe múltiplas recomendações e escolhe a melhor
- **Análise de riscos:** Avalia impactos antes de fazer mudanças
- **Documentação automática:** Gera relatórios detalhados das operações

## 🚀 Primeiros Passos

1. **Configure sua plataforma de IA** (Claude Desktop recomendado)
2. **Adicione sua chave LetsCloud** na configuração
3. **Reinicie a aplicação** da IA
4. **Teste com:** "Liste meus servidores atuais"
5. **Comece a usar naturalmente:** "Preciso de um servidor para..."

## 📞 Suporte

- **Documentação técnica:** Para desenvolvedores que querem integrar
- **Suporte LetsCloud:** Para questões sobre sua conta e faturamento
- **Comunidade MCP:** Para dúvidas sobre o protocolo MCP

## 🎉 Vantagens

✅ **Zero conhecimento técnico necessário**
✅ **Comunicação em português natural**
✅ **Execução automática de tarefas complexas**
✅ **Monitoramento 24/7 inteligente**
✅ **Otimização contínua de custos**
✅ **Suporte emergencial instantâneo**
✅ **Escalabilidade automática**
✅ **Backups e segurança automatizados**

Comece agora mesmo conversando naturalmente com sua IA sobre suas necessidades de infraestrutura! 