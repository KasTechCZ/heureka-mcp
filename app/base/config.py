from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GRAPHQL_URL: str = "https://searchapi3-search.search.prod.heu.group/graphql"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
