"""Serviço de busca semântica e geração de respostas (RAG)."""

import openai
from langchain_openai import ChatOpenAI
from loguru import logger

from app.core.config import settings
from app.services.semantic_search.config.settings import semantic_search_settings
from app.services.semantic_search.services.semantic_search import SemanticSearchService

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO":
"""


def get_service(api_key: str | None = None):
    return SemanticSearchService(
        documents_path=semantic_search_settings.DOCUMENTS_PATH,
        openai_api_key=api_key or settings.OPENAI_API_KEY,
        vectorstore_path=semantic_search_settings.VECTORSTORE_PATH,
    )


def vector_search(question: str):
    service = get_service()
    service.load_vectorstore()

    results = service.search(question, k=3)
    logger.info(f"Resultados da busca vetorial: {len(results)}")

    contexto = "\n\n".join([doc.content for doc in results])
    return contexto


def ask_question(question: str, api_key: str | None = None):
    try:
        contexto = vector_search(question)

        prompt = PROMPT_TEMPLATE.format(contexto=contexto, pergunta=question)

        llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            api_key=api_key or settings.OPENAI_API_KEY,
            temperature=0,
        )

        logger.info("Gerando resposta com LLM...")
        response = llm.invoke(prompt)

        return response.content

    except openai.AuthenticationError:
        logger.error("Erro de Autenticação: Verifique sua OPENAI_API_KEY.")
        return "Erro: Falha na autenticação com a API da OpenAI."
    except openai.RateLimitError:
        logger.error("Erro de Rate Limit: Limite de requisições excedido.")
        return "Erro: Limite de uso da OpenAI atingido. Tente novamente mais tarde."
    except openai.APIConnectionError:
        logger.error("Erro de Conexão: Não foi possível conectar à API da OpenAI.")
        return "Erro: Falha na conexão com o servidor da OpenAI."
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        return f"Desculpe, ocorreu um erro interno ao processar sua pergunta."
