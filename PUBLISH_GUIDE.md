# 📦 Guia de Publicação no PyPI

## Como Publicar o LetsCloud MCP Server no PyPI

### Pré-requisitos

1. **Conta no PyPI**:
   - Crie uma conta em [pypi.org](https://pypi.org/account/register/)
   - Ative a autenticação 2FA (obrigatório)

2. **Instalar ferramentas**:
   ```bash
   pip install build twine
   ```

### Passo a Passo

#### 1. Verificar o `pyproject.toml`
Nosso arquivo já está configurado corretamente:
```toml
[project]
name = "letscloud-mcp-server"
version = "1.0.0"
description = "LetsCloud MCP Server for infrastructure management"
# ... resto da configuração
```

#### 2. Construir o Pacote
```bash
# No diretório raiz do projeto
python -m build
```

Isso criará:
- `dist/letscloud_mcp_server-1.0.0.tar.gz` (código fonte)
- `dist/letscloud_mcp_server-1.0.0-py3-none-any.whl` (wheel)

#### 3. Verificar o Pacote
```bash
twine check dist/*
```

#### 4. Testar no TestPyPI (Opcional)
```bash
# Upload para o PyPI de teste
twine upload --repository testpypi dist/*

# Testar instalação
pip install --index-url https://test.pypi.org/simple/ letscloud-mcp-server
```

#### 5. Publicar no PyPI Real
```bash
twine upload dist/*
```

### Após a Publicação

Os usuários poderão instalar com:
```bash
pip install letscloud-mcp-server
```

## 🔧 Opções Alternativas (Sem PyPI)

### 1. Instalação via GitHub
```bash
pip install git+https://github.com/usuario/letscloud-mcp-server.git
```

### 2. Instalação Local
```bash
# Clone o repositório
git clone https://github.com/usuario/letscloud-mcp-server.git
cd letscloud-mcp-server

# Instale em modo desenvolvimento
pip install -e .
```

### 3. Distribuição como Zip
```bash
# Baixe e extraia o zip
# Então instale localmente
pip install .
```

## 📋 Checklist de Publicação

- [ ] Conta no PyPI criada e verificada
- [ ] 2FA ativado no PyPI
- [ ] `pyproject.toml` configurado
- [ ] Versão atualizada
- [ ] Documentação completa
- [ ] Testes funcionando
- [ ] Build realizado (`python -m build`)
- [ ] Verificação ok (`twine check dist/*`)
- [ ] Upload realizado (`twine upload dist/*`)

## ⚠️ Importantes

1. **Nome único**: `letscloud-mcp-server` deve estar disponível no PyPI
2. **Versionamento**: Use semantic versioning (1.0.0, 1.0.1, etc.)
3. **Dependências**: Todas especificadas no `pyproject.toml`
4. **Licença**: Arquivo LICENSE incluído
5. **README**: Documentação clara para usuários

## 🔄 Atualizações Futuras

Para publicar novas versões:
1. Atualize a versão no `pyproject.toml`
2. Execute `python -m build`
3. Execute `twine upload dist/*` 