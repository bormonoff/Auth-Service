import os
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Project root directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(os.path.dirname(BASE_DIR), ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_file_encoding="utf-8", extra="ignore"
    )

    # Postgres
    PG_USER: str = Field(default="Postgres_user")
    PG_PASSWORD: str = Field(default="Postgres_pasword")
    PG_HOST: str = Field(default="Postgres_host")
    PG_PORT: int = Field(default=9999)
    PG_DB: str = Field(default="Auth_DB")

    # Redis
    AUTH_REDIS_HOST: str = Field(default="fastapi-auth")
    AUTH_REDIS_PORT: int = Field(default="9998")

    # FastAPI
    AUTH_FASTAPI_HOST: str = Field(default="fastapi-auth")
    AUTH_FASTAPI_PORT: int = Field(default="8000")

    # Requests
    BASE_HEADERS: dict = {
        "content-type": "application/json",
        "accept": "application/json",
    }
    LOGIN_HEADERS: dict = {
        "content-type": "application/x-www-form-urlencoded",
        "accept": "application/json",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    }

    # Credentials
    ADMIN_LOGIN: str = Field(default="")
    ADMIN_PASSWORD: str = Field(default="")

    # Routes
    API_URL: str = "http://localhost:8000/api/v1"
    URL_LOGIN: str = "/auth/login"
    URL_REGISTER: str = "/profile/register"
    URL_PROFILE: str = "/profile/personal"
    URL_ROLES: str = "/roles"

    #JWT key
    JWT_SECRET: str = "Secret encode token"

@lru_cache
def get_settings():
    return Settings()
