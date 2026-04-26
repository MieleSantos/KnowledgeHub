# KnowledgeHub API

API REST em FastAPI para gerenciamento de um catalogo de livros com banco de dados SQLite.

## Stack

- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM para banco de dados
- **Pydantic** - Validacao de dados
- **SQLite** - Banco de dados
- **Poetry** - Gerenciamento de dependencias
- **Pytest** - Testes
- **Ruff** - Linter

## Requisitos

- Python 3.12+
- Poetry

## Instalacao

```bash
poetry install
```

## Executar a API

```bash
poetry run uvicorn app.main:app --reload
```

Base URL: `http://localhost:8000`  
Documentacao SWagger: `http://localhost:8000/docs`  
Rotas prefixadas com: `/api/v1`

## Comandos (taskipy)

```bash
poetry run task install   # Instala dependencias
poetry run task test    # Executa testes
poetry run task lint   # Verifica codigo
poetry run task format # Formata codigo
poetry run task check  # Lint +Test
```

## Endpoints

| Metodo | Rota | Descricao |
|--------|------|----------|
| POST | `/api/v1/books/` | Cria um livro |
| GET | `/api/v1/books/` | Lista todos os livros |
| GET | `/api/v1/books/author?author=<nome>` | Filtra por autor |
| GET | `/api/v1/books/titulo?titulo=<texto>` | Filtra por titulo |

## Estrutura do Projeto

```
app/
├── api/routers/      # Endpoints da API
├── core/             # Config e banco de dados
├── models/           # Modelos SQLAlchemy
├── repositories/    # Logica de acesso a dados
├── schemas/          # Schemas Pydantic
main.py              # Aplicacao FastAPI
tests/               # Testes
pyproject.toml       # Configuracao Poetry
```