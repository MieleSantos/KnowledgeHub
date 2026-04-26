from typing import List

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from loguru import logger


class VectorStoreRepository:
    """Repositório para gerenciamento do vector store FAISS.

    Responsável por criar, salvar, carregar e realizar buscas em índices vetoriais.
    """

    def __init__(self, openai_api_key: str):
        """Inicializa o repositório com o modelo de embeddings.

        Args:
            openai_api_key: Chave de API para o OpenAIEmbeddings.
        """
        self.embeddings = OpenAIEmbeddings(api_key=openai_api_key)
        self.vectorstore = None

    def create(self, documents: List[dict]) -> FAISS:
        """Cria um novo vector store a partir de uma lista de documentos.

        Args:
            documents: Lista de dicionários contendo 'content', 'id' e 'title'.

        Returns:
            FAISS: A instância do vector store criada.
        """
        logger.info(f"Creating vectorstore with {len(documents)} documents")
        docs = [
            Document(
                page_content=doc["content"],
                metadata={"id": doc["id"], "title": doc["title"]},
            )
            for doc in documents
        ]
        self.vectorstore = FAISS.from_documents(docs, self.embeddings)
        logger.success(f"Vectorstore created with {len(documents)} embeddings")
        return self.vectorstore

    def save(self, path: str) -> None:
        """Salva o vector store localmente no caminho especificado.

        Args:
            path: Diretório onde o índice será salvo.
        """
        if self.vectorstore:
            logger.info(f"Saving vectorstore to {path}")
            self.vectorstore.save_local(path)
            logger.success(f"Vectorstore saved to {path}")

    def load(self, path: str) -> None:
        """Carrega um vector store do disco.

        Args:
            path: Diretório onde o índice está armazenado.
        """
        logger.info(f"Loading vectorstore from {path}")
        self.vectorstore = FAISS.load_local(
            path, self.embeddings, allow_dangerous_deserialization=True
        )
        logger.success(f"Vectorstore loaded from {path}")

    def search(self, query: str, k: int = 3) -> List[dict]:
        """Realiza busca por similaridade de cosseno no índice.

        Args:
            query: Texto da busca.
            k: Número de documentos a retornar.

        Returns:
            List[dict]: Lista de documentos com metadados e score de distância.
        """
        if not self.vectorstore:
            raise ValueError("Vectorstore not initialized")

        logger.info(f"Searching for: '{query}' (k={k})")
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        logger.success(f"Found {len(results)} results")

        return [
            {
                "id": doc.metadata["id"],
                "title": doc.metadata["title"],
                "content": doc.page_content,
                "score": score,
            }
            for doc, score in results
        ]
