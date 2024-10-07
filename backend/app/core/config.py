from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class CeleryConfig(BaseModel):
    broker_url: str = "redis://localhost:6379/1"
    result_backend: str = "redis://localhost:6379/2"
    broker_connection_retry_on_startup: bool = True


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
        env_nested_delimiter="__",
    )
    api_v1_str: str = "/api/v1"

    qdrant_url: str = "http://localhost:6333"
    qdrant_collection_name: str = "documents"
    qdrant_result_count: int = 3

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimensions: int = 384

    celery: CeleryConfig = CeleryConfig()


settings = Settings()  # type: ignore
