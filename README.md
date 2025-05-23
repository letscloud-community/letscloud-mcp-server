# LetsCloud MCP API

Este é o projeto da API do MCP (Model Context Protocol) da LetsCloud. Esta API permite a integração com o servidor MCP para gerenciamento de recursos na LetsCloud.

## Estrutura do Projeto

```
letscloud-mcp/
├── app/
│   ├── api/          # Endpoints da API
│   ├── core/         # Configurações core
│   ├── models/       # Modelos de dados
│   ├── services/     # Serviços da aplicação
│   └── main.py       # Ponto de entrada da aplicação
└── README.md
```

## Requisitos

- Python 3.11+
- FastAPI
- Uvicorn
- Outras dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/letscloud/letscloud-mcp.git
cd letscloud-mcp
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

Para usar esta API, você precisará:

1. Ter acesso a um servidor MCP (fornecido pela LetsCloud)
2. Obter suas credenciais de acesso
3. Configurar as variáveis de ambiente necessárias

### Exemplo de Uso

```python
from letscloud_mcp import LetsCloudMCP

# Inicializar o cliente
mcp = LetsCloudMCP(
    server_url="https://mcp.letscloud.io",
    api_token="seu_token_aqui"
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

## Licença

Este projeto é licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Suporte

Para suporte, entre em contato com:
- Email: support@letscloud.io
- Documentação: https://letscloud.io/help 