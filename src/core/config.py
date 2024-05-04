import os
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(os.path.dirname(BASE_DIR), ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_file_encoding="utf-8", extra="ignore"
    )

    # Postgres
    PG_USER: str = Field(default="Postgres_user")
    PG_PASSWORD: str = Field(default="Postgres_pasword")
    PG_HOST: str = Field(default="Postgres_host")
    PG_PORT: int = Field(default="9999")
    PG_DB: str = Field(default="Auth_DB")

    # Redis
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default="9998")

    # Настройки Swagger-документации
    URL_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = Field(default="Auth-service")
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Authetification service."
    OPEN_API_DOCS_URL: str = "/auth/docs"
    OPEN_API_URL: str = "/auth/openapi.json"

    # FastAPI
    AUTH_FASTAPI_HOST: str = Field(default="fastapi-auth")
    AUTH_FASTAPI_PORT: int = Field(default="8000")

    # JWT
    JWT_SECRET: str = Field(default="Secret encode token")

    @property
    def postgres_dsn(self) -> str:
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"


@lru_cache
def get_settings():
    return Settings()
