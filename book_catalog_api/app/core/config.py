from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./books.db"
    APP_NAME: str = "Library Book API"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_TEMPERATURE: float = 0.2


settings = Settings()
