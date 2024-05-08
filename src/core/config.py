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
    AUTH_REDIS_HOST: str = Field(default="fastapi-auth")
    AUTH_REDIS_PORT: int = Field(default="9998")

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
    JWT_CODE: str = Field(default="utf-8")
    # Acess token lifetime in hours
    ACESS_TOKEN_LIFETIME: int = Field(default=2)
    # Acess token lifetime in days
    REFRESH_TOKEN_LIFETIME: int = Field(default=14)
    # Validation config
    LOGIN_MIN_LENGTH: int = 5
    LOGIN_MAX_LENGTH: int = 50
    LOGIN_PATTERN: str = (
        f"^[A-Za-z0-9_-]{{{LOGIN_MIN_LENGTH},{LOGIN_MAX_LENGTH}}}$"
    )
    PASSWORD_MIN_LENGTH: int = 5
    PASSWORD_MAX_LENGTH: int = 50
    HASHED_PASSWORD_MAX_LENGTH: int = 255
    FIRST_NAME_MAX_LENGTH: int = 255
    LAST_NAME_MAX_LENGTH: int = 255

    @property
    def postgres_dsn(self) -> str:
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"


@lru_cache
def get_settings():
    return Settings()
