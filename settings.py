from functools import lru_cache
from typing import ClassVar

from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=find_dotenv(), extra="ignore"
    )

    # OPENAI
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = ""

    # GitHub
    GITHUB_API_KEY: str
    GITHUB_BASE_URL: str

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: str = 6379

    # API
    API_PORT: int = 8005
    API_HOST: str = "0.0.0.0"
    API_DEBUG: bool = True

    # DOCS
    DOCS_TITLE: str = "CodeReviewAI"
    DOCS_DESCRIPTION: str = ""

    DOCS_URL: str | None = None
    REDOCS_URL: str | None = None
    OPENAPI_URL: str | None = None


@lru_cache()
def get_settings() -> Settings:
    return Settings()
