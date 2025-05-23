# LetsCloud MCP API

API para gerenciamento de servidores LetsCloud.

## Descrição
Esta aplicação fornece uma API para gerenciar servidores, snapshots e chaves SSH na LetsCloud, servindo como um proxy seguro para operações automatizadas.

## Instalação

```bash
git clone https://github.com/seu-usuario/letscloud-mcp.git
cd letscloud-mcp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuração

A aplicação requer algumas variáveis de ambiente para funcionar corretamente. As credenciais sensíveis serão gerenciadas automaticamente pelo servidor MCP.

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Server settings
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=true

# Security settings
JWT_SECRET=<fornecido pela IA>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database settings
DATABASE_URL=sqlite:///./app.db

# Redis settings
REDIS_URL=redis://localhost:6379/0
```

> **Nota**: As credenciais sensíveis serão gerenciadas automaticamente pelo servidor MCP. Não é necessário configurá-las manualmente.

## Integração com o Servidor MCP

Para integrar esta API ao servidor MCP, siga os seguintes passos:

1. **Preparação do Ambiente**
   ```bash
   # No diretório do servidor MCP
   cd ../mcp-server
   
   # Criar diretório para a API
   mkdir -p apps/letscloud-mcp
   
   # Copiar os arquivos da API
   cp -r ../letscloud-mcp/* apps/letscloud-mcp/
   ```

2. **Configuração do Nginx**
   Adicione a seguinte configuração ao arquivo `nginx/conf.d/letscloud-mcp.conf`:
   ```nginx
   location /api/letscloud/ {
       proxy_pass http://localhost:8000/;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_set_header X-Forwarded-Proto $scheme;
   }
   ```

3. **Configuração do Supervisor**
   Crie um arquivo `supervisor/conf.d/letscloud-mcp.conf`:
   ```ini
   [program:letscloud-mcp]
   command=/path/to/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
   directory=/path/to/mcp-server/apps/letscloud-mcp
   user=www-data
   autostart=true
   autorestart=true
   stderr_logfile=/var/log/supervisor/letscloud-mcp.err.log
   stdout_logfile=/var/log/supervisor/letscloud-mcp.out.log
   environment=PYTHONPATH="/path/to/mcp-server/apps/letscloud-mcp"
   ```

4. **Reiniciar Serviços**
   ```bash
   # Recarregar configuração do Nginx
   sudo nginx -t && sudo systemctl reload nginx
   
   # Recarregar Supervisor
   sudo supervisorctl reread
   sudo supervisorctl update
   sudo supervisorctl start letscloud-mcp
   ```

5. **Verificação**
   - Acesse `https://seu-mcp-server/api/letscloud/docs` para verificar se a API está funcionando
   - Verifique os logs em `/var/log/supervisor/letscloud-mcp.*.log`

## Executando a aplicação

```bash
uvicorn app.main:app --reload
```

Acesse a documentação interativa em: [http://localhost:8000/docs](http://localhost:8000/docs)

## Executando os testes

```bash
./run_tests.sh
```

## Estrutura do Projeto

- `app/` - Código principal da aplicação
- `tests/` - Testes automatizados
- `requirements.txt` - Dependências
- `run_tests.sh` - Script para rodar os testes

## Licença

MIT

## Requisitos

- Python 3.11+
- FastAPI
- Uvicorn
- Outras dependências listadas em `requirements.txt`

## Uso

Para usar esta API, você precisará:

1. Ter acesso a um servidor MCP (fornecido pela LetsCloud)
2. Configurar as variáveis de ambiente necessárias

### Exemplo de Uso

```python
from letscloud_mcp import LetsCloudMCP

# Inicializar o cliente
mcp = LetsCloudMCP(
    server_url="https://mcp.letscloud.io"
)

# Usar os métodos da API
response = mcp.list_servers()
```

## Documentação da API

A documentação completa da API está disponível em:
- Swagger UI: `https://mcp.letscloud.io/docs`
- ReDoc: `https://mcp.letscloud.io/redoc`

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

## Suporte

Para suporte, entre em contato com:
- Email: support@letscloud.io
- Documentação: https://letscloud.io/help 