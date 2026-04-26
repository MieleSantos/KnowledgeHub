from loguru import logger

from app.services.semantic_search.repositories.document_loader import DocumentLoader
from app.services.semantic_search.repositories.vector_store import VectorStoreRepository
from app.services.semantic_search.schemas.search import SearchResult


class SemanticSearchService:
    """Serviço responsável pela orquestração da busca semântica.

    Esta classe coordena o carregamento de documentos, criação, persistência
    e busca no vector store.
    """

    def __init__(
        self,
        documents_path: str,
        openai_api_key: str,
        vectorstore_path: str = "vectorstore",
    ):
        """Inicializa o serviço de busca semântica.

        Args:
            documents_path: Caminho para o arquivo de documentos (JSON).
            openai_api_key: Chave de API da OpenAI.
            vectorstore_path: Caminho para persistência do vector store.
        """
        self.documents_path = documents_path
        self.vectorstore_path = vectorstore_path
        self.document_loader = DocumentLoader()
        self.vector_store = VectorStoreRepository(openai_api_key)

    def initialize(self) -> None:
        """Realiza o setup inicial do serviço.

        Lê os documentos do disco, gera os embeddings e salva o vector store localmente.
        """
        logger.info("Initializing semantic search service")
        documents = self.document_loader.load(self.documents_path)
        self.vector_store.create(documents)
        self.vector_store.save(self.vectorstore_path)
        logger.success("Semantic search service initialized")

    def load_vectorstore(self, path: str = None) -> None:
        """Carrega um vector store existente do disco.

        Args:
            path: Caminho opcional do vector store. Se omitido, usa o path padrão.
        """
        path = path or self.vectorstore_path
        logger.info(f"Loading vectorstore from {path}")
        self.vector_store.load(path)
        logger.success("Vectorstore loaded")

    def save_vectorstore(self, path: str = None) -> None:
        """Salva o estado atual do vector store no disco.

        Args:
            path: Caminho opcional para salvar. Se omitido, usa o path padrão.
        """
        path = path or self.vectorstore_path
        logger.info(f"Saving vectorstore to {path}")
        self.vector_store.save(path)
        logger.success("Vectorstore saved")

    def search(self, query: str, k: int = 3) -> list[SearchResult]:
        """Realiza uma busca por similaridade no vector store.

        Args:
            query: Texto da consulta.
            k: Número de resultados a retornar.

        Returns:
            list[SearchResult]: Lista de documentos encontrados com seus scores.
        """
        logger.info(f"Searching for: '{query}'")
        results = self.vector_store.search(query, k=k)
        return [SearchResult(**r) for r in results]
