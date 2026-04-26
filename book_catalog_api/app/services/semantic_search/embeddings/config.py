"""Configuração do modelo de embeddings da OpenAI."""

from langchain_openai import OpenAIEmbeddings
from loguru import logger

from config.settings import settings


def get_embeddings():
    """Cria uma instância do modelo de embeddings da OpenAI.

    Returns:
        OpenAIEmbeddings: Instância do modelo de embeddings.
    """
    logger.info(f"Creating OpenAI embeddings: {settings.OPENAI_EMBEDDING_MODEL}")
    return OpenAIEmbeddings(
        model=settings.OPENAI_EMBEDDING_MODEL,
        api_key=settings.OPENAI_API_KEY,
    )
