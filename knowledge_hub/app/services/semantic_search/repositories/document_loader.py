import json
from typing import Any, Dict, List

from loguru import logger


class DocumentLoader:
    """Classe responsável pelo carregamento de documentos de fontes externas."""

    @staticmethod
    def load(path: str) -> List[Dict[str, Any]]:
        """Lê um arquivo JSON contendo documentos e retorna uma lista de dicionários.

        Args:
            path: Caminho para o arquivo .json.

        Returns:
            List[Dict[str, Any]]: Lista de documentos carregados.
        """
        logger.info(f"Loading documents from {path}")
        with open(path, "r", encoding="utf-8") as f:
            documents = json.load(f)
        logger.info(f"Loaded {len(documents)} documents")
        return documents
