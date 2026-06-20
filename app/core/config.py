from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Nexus CRM Backend"
    api_prefix: str = "/api/v1"
    database_url: str = "postgresql+psycopg2://postgres:root@localhost:5432/crm"
    jwt_secret: str = "change-me"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 14
    cors_origins: str = "http://localhost:5173,http://localhost:5174, http://localhost:3000"
    redis_url: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
