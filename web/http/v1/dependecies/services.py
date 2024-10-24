from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis

from settings import Settings
from src.services.cache import CacheService
from src.services.github import GitHubIntegrationService
from src.services.openai import OpenAIIntegrationService
from src.services.review import ReviewService
from web.http.v1.dependecies.redis import get_redis_client
from web.http.v1.dependecies.settings import get_api_settings


def get_github_integration_service(
        settings: Settings
) -> GitHubIntegrationService:
    return GitHubIntegrationService(
        settings=settings
    )


def get_openai_integration_service(
        settings: Settings
) -> OpenAIIntegrationService:
    return OpenAIIntegrationService(
        settings=settings
    )


def get_cache_service(redis_client: Redis) -> CacheService:
    return CacheService(
        redis_client=redis_client
    )


def get_review_service(settings: Annotated[Settings, Depends(get_api_settings)],
                       redis_client: Annotated[Redis, Depends(get_redis_client)]
                       ) -> ReviewService:
    return ReviewService(
        github_service=get_github_integration_service(settings),
        openai_service=get_openai_integration_service(settings),
        cache_service=get_cache_service(redis_client=redis_client)
    )
