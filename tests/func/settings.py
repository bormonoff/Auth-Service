import os
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Project root directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{BASE_DIR}/.env", env_file_encoding="utf-8", extra="ignore"
    )

    # Postgres
    PG_USER: str = Field(default="Postgres_user")
    PG_PASSWORD: str = Field(default="Postgres_pasword")
    PG_HOST: str = Field(default="Postgres_host")
    PG_PORT: int = Field(default=8002)
    PG_DB: str = Field(default="Auth_DB")

    # Redis
    AUTH_REDIS_HOST: str = Field(default="fastapi-auth")
    AUTH_REDIS_PORT: int = Field(default=8001)

    # FastAPI
    AUTH_FASTAPI_HOST: str = Field(default="fastapi-auth")
    AUTH_FASTAPI_PORT: int = Field(default="8000")

    # Credentials
    ADMIN_LOGIN: str = Field(default="")
    ADMIN_PASSWORD: str = Field(default="")

    # Routes
    API_URL: str = "http://localhost:8000/api/v1"

    # JWT key
    JWT_SECRET: str = "Secret encode token"
    JWT_CODE: str = Field(default="utf-8")


@lru_cache
def get_settings():
    return Settings()
