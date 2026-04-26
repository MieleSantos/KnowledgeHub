# 📚 KnowledgeHub

Sistema de gerenciamento de biblioteca com integração de IA para busca semântica e chatbot.

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (Streamlit)                   │
│                     http://localhost:8501                   │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP
                          ▼
┌─────────────────────────────────────────────────────� �───┐
│                      Backend (FastAPI)                      │  
│                     http://localhost:8000                   │
│  ┌─────────────┐ ┌─────────────┐ ┌────────────────────────┐ │
│  │   Books     │ │  Chatbot    │ │  Semantic Search (RAG) │ │ 
│  │   CRUD      │ │  AI Tutor   │ │  Vector Store + LLM    │ │
│  └─────────────┘ └─────────────┘ └────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Services Layer (Business Logic)        │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Data Layer (SQLAlchemy + FAISS)        │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## 📋 Funcionalidades

### 📚 Biblioteca de Livros
- CRUD completo de livros (criar, listar, buscar, detalhe)
- Paginação e busca por título/autor
- Validação com Pydantic

### 🤖 Chatbot Python
- Tutor de Python baseado em LLM (OpenAI)
- Respostas com boas práticas
- Histórico de conversa

### 🔎 Busca Semântica (RAG)
- Indexação de documentos em vector store (FAISS)
- Embeddings OpenAI
- Busca por similaridade de cossenos

## 🛠️ Tecnologias

| Componente | Tecnologia | Versão |
|-----------|------------|---------|
| Backend API | FastAPI | 0.109+   |
| ORM | SQLAlchemy | 2.0+ |        |
| Validação | Pydantic v2 | 2.0+   |
| Vector Store | FAISS |- |        |
| LLM | LangChain + OpenAI | -     |
| Frontend | Streamlit | 1.28+     |
| Container | Docker Compose | -   |

## 📁 Estrutura do Projeto

```
backend_python_ia/
├── knowledge_hub/
│   ├── app/
│   │   ├── api/routers/       # Rotas FastAPI
│   │   ├── core/             # Config, database
│   │   ├── integrations/     # Lógica IA
│   │   ├── models/           # SQLAlchemy models
│   │   ├── repositories/    # Acesso a dados
│   │   ├── schemas/         # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── tests/              # Testes
│   ├── Dockerfile
│   └── pyproject.toml
├── streamlit_hub/
│   ├── app.py              # Interface Streamlit
│   ├── Dockerfile
│   └── pyproject.toml
├── docker-compose.yml
├── .env                   # Variáveis de ambiente
└── README.md
```

## 🚀 Como Executar

### Pré-requisitos
- Docker e Docker Compose instalados
- OpenAI API Key

### 1. Configurar variáveis de ambiente

```bash
cp .env.example .env
# Edite o .env e adicione sua OpenAI API Key
```

### 2. Subir os containers

```bash
docker compose up -d
```

### 3. Acessar as aplicações

| Serviço | URL |
|---------|-----|
| API | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |
| Frontend | http://localhost:8501 |

### 4. (Opcional) Configurar API Key no Frontend

1. Abra http://localhost:8501
2. Na barra lateral, expanda "🔑 OpenAI Key"
3. Cole sua API key

## 🧪 Endpoints da API

### Livros
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/v1/books/` | Criar livro |
| GET | `/api/v1/books/` | Listar livros (paginação + busca) |
| GET | `/api/v1/books/{id}` | Detalhe do livro |

### IA
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/v1/chatbot/ask` | Pergunta ao chatbot |
| POST | `/api/v1/semantic-search/ingest` | Indexar documentos |
| POST | `/api/v1/semantic-search/ask` | Busca semântica |

## 🏋️ Melhores Práticas

### Python (seguindo python-patterns)
- **Async/Await**: Usar para operações I/O-bound
- **Type Hints**: Sempre em APIs públicas e funções
- **Pydantic**: Validação de requests/responses
- **Separação de camadas**: routers → services → repositories

### API Design
- **RESTful**: Métodos HTTP corretos
- **Response model**: Tipos definidos com Pydantic
- **Error handling**: HTTPException com status codes

### Código Limpo
- Sem comentários desnecessários
- Nomes descritivos
- Funções pequenas e focadas
- DRY (Don't Repeat Yourself)

## 📝 Exemplos de Uso

### Criar livro via API
```bash
curl -X POST http://localhost:8000/api/v1/books/ \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Python Fluente", "autor": "Luciano Ramalho"}'
```

### Listar livros
```bash
curl "http://localhost:8000/api/v1/books/?page=1&size=10&q=Python"
```

### Buscar semanticamente
```bash
curl -X POST http://localhost:8000/api/v1/semantic-search/ask \
  -H "Content-Type: application/json" \
  -H "X-OpenAI-Key: sk-..." \
  -d '{"question": "O que são embeddings?"}'
```

## 🔧 Desenvolvimento Local

### Sem Docker

```bash
# Backend
cd knowledge_hub
poetry install
poetry run uvicorn app.main:app --reload

# Frontend
cd streamlit_hub
poetry install
poetry run streamlit run app.py
```

## 📄 Licença

MIT