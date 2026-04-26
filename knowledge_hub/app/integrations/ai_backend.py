"""Integrações com serviços de IA."""

from langchain_openai import ChatOpenAI

from app.core.config import settings

SYSTEM_PROMPT = """
Voce e um tutor especialista em Python.
Seu objetivo e ajudar iniciantes e pessoas intermediarias com duvidas tecnicas.

Diretrizes:
- Responda em portugues do Brasil, com tom didatico, claro e objetivo.
- Priorize melhores praticas de Python (legibilidade, simplicidade, tipagem quando fizer sentido, tratamento de erros e testes).
- Quando houver codigo, mostre exemplos curtos e executaveis.
- Explique o por que das recomendacoes, nao apenas o como.
- Se a pergunta estiver ambigua, faca 1 pergunta curta de esclarecimento antes de seguir.
- Se nao souber algo com seguranca, diga explicitamente e sugira como validar.
- Evite inventar APIs, funcoes ou bibliotecas inexistentes.
""".strip()


def get_api_key(api_key: str | None = None) -> str:
    if api_key:
        return api_key
    if settings.OPENAI_API_KEY:
        return settings.OPENAI_API_KEY
    raise ValueError("OPENAI_API_KEY nao configurada.")


def get_chat_model(api_key: str | None = None) -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.OPENAI_MODEL,
        api_key=get_api_key(api_key),
        temperature=settings.OPENAI_TEMPERATURE,
    )


def ask_chatbot(question: str, api_key: str | None = None) -> str:
    llm = get_chat_model(api_key)
    response = llm.invoke([("system", SYSTEM_PROMPT), ("human", question)])
    return response.content


def ingest_semantic_documents() -> str:
    from app.services.semantic_search.services.ingest import ingest_documents
    ingest_documents()
    return "Ingestao concluida com sucesso."


def ask_semantic_search(question: str, api_key: str | None = None) -> str:
    from app.services.semantic_search.services.search import ask_question
    return ask_question(question, api_key=get_api_key(api_key))
