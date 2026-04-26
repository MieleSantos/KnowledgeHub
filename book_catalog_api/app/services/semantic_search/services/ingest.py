"""Serviço de ingestão de documentos no vector store."""

from loguru import logger

from app.core.config import settings
from app.services.semantic_search.config.settings import semantic_search_settings
from app.services.semantic_search.services.semantic_search import SemanticSearchService


def ingest_documents():
    service = SemanticSearchService(
        documents_path=semantic_search_settings.DOCUMENTS_PATH,
        openai_api_key=settings.OPENAI_API_KEY,
        vectorstore_path=semantic_search_settings.VECTORSTORE_PATH,
    )
    service.initialize()
