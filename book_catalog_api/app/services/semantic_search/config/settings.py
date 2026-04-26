from pydantic_settings import BaseSettings, SettingsConfigDict


class SemanticSearchSettings(BaseSettings):
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"

    VECTORSTORE_PATH: str = "/app/data/vectorstore"
    DOCUMENTS_PATH: str = "/app/data/documents.json"

    model_config = SettingsConfigDict(extra="ignore")


semantic_search_settings = SemanticSearchSettings()

