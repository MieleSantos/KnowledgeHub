# KnowledgeHub (Streamlit)

Frontend Streamlit que consome um backend FastAPI.

Arquitetura:

- `streamlit_hub`: frontend (UI)
- `knowledge_hub`: backend com rotas de livros, chatbot e busca semantica
- `semantic_search`: base RAG utilizada pelo backend

## Executar com Docker Compose (recomendado)

Na raiz `backend_python_ia`, crie/edite um `.env` com:

```env
OPENAI_API_KEY=sk-...
```

Depois rode:

```bash
docker compose up --build
```

Servicos:

- Hub Streamlit: `http://localhost:8501`
- API FastAPI: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`

## Menu da interface

- **Chatbot**: chama `POST /api/v1/chatbot/ask`
- **API**: mostra resultado de listar livros (`GET`) e criar livro (`POST`)
- **Busca Semantica**: chama ingestao e pergunta via API

## Rotas novas no backend

- `GET /api/v1/health`
- `POST /api/v1/chatbot/ask`
- `POST /api/v1/semantic-search/ingest`
- `POST /api/v1/semantic-search/ask`
