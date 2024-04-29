from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Postgres
    pg_user: str
    pg_password: str
    pg_host: str
    pg_port: int
    pg_db: str

    model_config = SettingsConfigDict(env_file="src/.env")


@lru_cache
def get_settings():
    return Settings()
