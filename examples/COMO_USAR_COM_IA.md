# Como Usar LetsCloud MCP Server com IA

Guia completo para configurar e usar o LetsCloud MCP Server em diferentes plataformas de IA.

## 🎯 Visão Geral

O LetsCloud MCP Server permite que você gerencie sua infraestrutura de servidores através de **conversas naturais** com IA. Não precisa saber programação ou comandos técnicos - apenas converse normalmente!

### O que você pode fazer:
- **"Crie um servidor para minha loja online"**
- **"Meu site está lento, ajude-me a resolver"** 
- **"Faça backup de todos os meus servidores"**
- **"Preciso que meu site aguente mais tráfego"**
- **"Socorro! Meu site saiu do ar!"**

## 🔧 Configuração por Plataforma

### 1. Claude Desktop (Mais Fácil - Recomendado)

#### Passo 1: Instalar Claude Desktop
- Baixe em: https://claude.ai/download
- Instale e crie uma conta

#### Passo 2: Obter sua chave LetsCloud
1. Acesse: https://cloud.letscloud.io/account/api
2. Clique em "Gerar Nova Chave API"
3. Copie o token (começa com `let_`)

#### Passo 3: Configurar o MCP Server
1. **Encontre o arquivo de configuração:**
   - **Windows**: Abra `%APPDATA%\Claude\claude_desktop_config.json`
   - **Mac**: Abra `~/Library/Application Support/Claude/claude_desktop_config.json`  
   - **Linux**: Abra `~/.config/claude/claude_desktop_config.json`

2. **Cole esta configuração:**
   ```json
   {
     "mcpServers": {
       "letscloud": {
         "command": "python",
         "args": ["-m", "letscloud_mcp_server"],
         "env": {
           "LETSCLOUD_API_TOKEN": "cole-seu-token-aqui"
         }
       }
     }
   }
   ```

3. **Substitua** `cole-seu-token-aqui` pelo seu token real

#### Passo 4: Instalar o MCP Server
Abra o terminal/prompt de comando e execute:
```bash
pip install letscloud-mcp-server
```

#### Passo 5: Reiniciar e Testar
1. Feche completamente o Claude Desktop
2. Abra novamente
3. Digite: **"Liste meus servidores atuais"**
4. Se funcionou, você verá a lista de servidores! 🎉

### 2. OpenAI ChatGPT (Futuro)

**Status:** Em desenvolvimento
- Aguardando aprovação na GPT Store
- Para empresas: Contate suporte para integração custom

### 3. Outros Clientes MCP

O MCP Server funciona com qualquer aplicação que suporte o protocolo MCP:
- **Cline** (extensão do VS Code)
- **Zed Editor**
- **Continue** (VS Code)
- Qualquer cliente MCP compatível

## 💬 Como Conversar com a IA

### Linguagem Natural - Exemplos Reais

#### Para Iniciantes:
```
Você: "Oi! Sou novo aqui e preciso de um servidor para meu site"

IA: "Olá! Vou te ajudar a criar seu primeiro servidor. Algumas perguntas:
- Que tipo de site você quer criar?
- Quantos visitantes espera por mês?
- Qual seu orçamento?"

Você: "É um blog pessoal, uns 100 visitantes por mês, orçamento R$ 50"

IA: "Perfeito! Vou criar um servidor básico ideal para você:
✅ Servidor criado com 1GB RAM
✅ WordPress instalado automaticamente
✅ SSL gratuito configurado
✅ Custo: R$ 25/mês (dentro do orçamento!)
Quer que eu configure seu domínio também?"
```

#### Para E-commerce:
```
Você: "Tenho uma loja virtual que está crescendo muito, às vezes fica lenta"

IA: "Que ótimo que está crescendo! Vou analisar sua situação:
- Quantos visitantes únicos por dia você tem agora?
- Quantos produtos na loja?
- Em que horários nota mais lentidão?"

Você: "Uns 500 visitantes por dia, 200 produtos, fica lento à noite"

IA: "Identifiquei o problema! Você precisa escalar. Vou implementar:
🏗️ Load balancer para distribuir tráfego
🚀 Servidor adicional para horários de pico  
⚡ Cache inteligente para produtos
💰 Custo: +R$ 45/mês, mas site 3x mais rápido
Quer que eu implemente agora?"
```

#### Para Emergências:
```
Você: "SOCORRO! Meu site saiu do ar e tenho clientes esperando!"

IA: "🚨 EMERGÊNCIA! Já estou investigando...

🔍 Diagnóstico em 30 segundos:
- Servidor principal: Não responde ❌
- Causa: Sobrecarga de CPU
- Solução: Migração emergencial ⚡

🔄 Recuperando AGORA:
- Criando servidor emergencial (2 min)
- Restaurando backup mais recente (3 min)  
- Redirecionando tráfego (1 min)

✅ RESOLVIDO! Seu site voltou ao ar.
Total de indisponibilidade: 6 minutos
Vou configurar proteção contra futuras sobrecargas."
```

## 🛠️ Tipos de Pedidos que Funcionam

### Criação de Servidores
- "Crie um servidor para WordPress"
- "Preciso de um servidor para minha loja Magento"
- "Quero hospedar uma aplicação Node.js"
- "Crie um servidor de desenvolvimento"

### Gerenciamento
- "Liste todos os meus servidores"
- "Qual servidor está usando mais recursos?"
- "Reinicie o servidor da loja virtual"
- "Aumente a memória do servidor principal"

### Backups e Segurança
- "Faça backup de tudo agora"
- "Quando foi o último backup?"
- "Restaure o site de ontem"
- "Configure backup automático semanal"

### Monitoramento
- "Como está a performance dos servidores?"
- "Meu site está lento, por quê?"
- "Quais servidores estão sobrecarregados?"
- "Preciso de alertas quando algo der errado"

### Otimização
- "Como posso reduzir custos?"
- "Otimize a performance do site"
- "Preciso que meu site aguente mais tráfego"
- "Configure cache para acelerar o site"

## 🎯 Casos de Uso Específicos

### Blog Pessoal
```
"Quero criar um blog sobre culinária"
→ IA cria servidor otimizado para WordPress
→ Instala tema para blogs
→ Configura SEO básico
→ R$ 25/mês
```

### Loja Virtual
```
"Preciso de uma loja online para vender roupas"
→ IA cria infraestrutura para e-commerce
→ Instala WooCommerce ou Magento
→ Configura pagamentos (PIX, cartão)
→ R$ 65/mês
```

### Site Empresarial
```
"Quero um site profissional para minha empresa"
→ IA cria servidor empresarial
→ Instala CMS adequado
→ Configura formulários de contato
→ SSL premium e backup avançado
→ R$ 89/mês
```

### Aplicação Web
```
"Desenvolvei uma app em React, preciso hospedar"
→ IA analisa os requisitos técnicos
→ Configura ambiente Node.js
→ Configura CI/CD para deploys
→ R$ 75/mês
```

## 🔒 Configuração Avançada (Opcional)

### Para Recursos Extras de IA

Se quiser recursos ainda mais avançados, configure também:

```bash
# Para análises inteligentes com OpenAI
OPENAI_API_KEY="sk-seu-token-openai"

# Para comparação de soluções com Claude
ANTHROPIC_API_KEY="sk-ant-seu-token-claude"

# Para receber alertas por email
ALERT_EMAIL="seu-email@empresa.com"

# Para notificações no Slack
SLACK_WEBHOOK_URL="https://hooks.slack.com/..."
```

**Como obter essas chaves:**

**OpenAI:**
1. Acesse: https://platform.openai.com/api-keys
2. Clique "Create new secret key"
3. Copie a chave (começa com `sk-`)

**Anthropic:**
1. Acesse: https://console.anthropic.com/
2. Vá em "API Keys" → "Create Key"  
3. Copie a chave (começa com `sk-ant-`)

### Configuração Completa

```json
{
  "mcpServers": {
    "letscloud": {
      "command": "python",
      "args": ["-m", "letscloud_mcp_server"],
      "env": {
        "LETSCLOUD_API_TOKEN": "let_seu-token-letscloud",
        "OPENAI_API_KEY": "sk-seu-token-openai",
        "ANTHROPIC_API_KEY": "sk-ant-seu-token-claude",
        "ALERT_EMAIL": "admin@seudominio.com"
      }
    }
  }
}
```

## 🚨 Resolução de Problemas

### Erro: "MCP server not found"
✅ **Solução:** Instale o servidor MCP:
```bash
pip install letscloud-mcp-server
```

### Erro: "Invalid API token"
✅ **Solução:** Verifique se copiou o token completo da LetsCloud

### Erro: "Connection failed" 
✅ **Solução:** Reinicie Claude Desktop após configurar

### IA não responde sobre servidores
✅ **Solução:** Digite exatamente: "Liste meus servidores LetsCloud"

### Configuração não funcionou
✅ **Solução:** 
1. Verifique se o arquivo JSON está válido
2. Reinicie Claude Desktop completamente
3. Teste com comando simples primeiro

## 💡 Dicas para Melhor Experiência

### ✅ Funciona Bem:
- **Seja específico:** "Crie um servidor WordPress de 2GB RAM"
- **Contextualize:** "Minha loja tem 1000 visitantes/dia"
- **Peça ajuda:** "Não sei qual servidor preciso, me ajude"

### ❌ Evite:
- Comandos técnicos: "kubectl apply -f deployment.yaml"
- Jargão complexo: "Configure o ingress controller"
- Vagueza total: "Faça alguma coisa"

### 🎯 Exemplos Perfeitos:
```
✅ "Meu site WordPress está lento para 500 visitantes/dia"
✅ "Preciso de backup automático para minha loja online"
✅ "Quero um servidor que aguente picos de tráfego"
✅ "Socorro! Meu site saiu do ar!"
❌ "Configure nginx com load balancing"
❌ "Otimize a infraestrutura"
❌ "Faça alguma coisa"
```

## 🎉 Pronto para Começar!

1. **Configure Claude Desktop** com sua chave LetsCloud
2. **Reinicie a aplicação**
3. **Digite:** "Liste meus servidores atuais"
4. **Se funcionou:** Comece a conversar naturalmente!
5. **Se não funcionou:** Verifique os passos de configuração

**Primeira conversa sugerida:**
```
"Oi! Sou novo no LetsCloud MCP Server. Pode me mostrar meus servidores atuais e me ajudar a entender como posso melhorar minha infraestrutura?"
```

A partir daí, converse naturalmente sobre suas necessidades! 🚀 