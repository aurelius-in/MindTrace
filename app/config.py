from pydantic import BaseSettings, Field
from functools import lru_cache


class Settings(BaseSettings):
    # Core App Settings
    app_env: str = Field("development", env="APP_ENV")
    secret_key: str = Field(..., env="SECRET_KEY")
    log_level: str = Field("info", env="LOG_LEVEL")

    # OpenAI / LLM Settings
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")

    # Vector DB
    vector_db_path: str = Field("./data/vectors.faiss", env="VECTOR_DB_PATH")

    # Optional Features
    enable_analytics: bool = Field(False, env="ENABLE_ANALYTICS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Cached instance so settings are loaded only once
@lru_cache()
def get_settings():
    return Settings()


# Global settings instance
settings = get_settings()
