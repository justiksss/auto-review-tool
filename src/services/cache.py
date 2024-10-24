from enum import StrEnum

from orjson import dumps, loads
from pydantic import BaseModel
from redis.asyncio import Redis

from src.models.github import GitHubFileContent
from src.services.base import BaseService


class CachePrefixes(StrEnum):
    github = "github"


class CacheService(BaseService):
    """Implement the cache service using redis"""
    cache_ttl = 60 * 60

    def __init__(self, redis_client: Redis) -> None:
        self.redis_client = redis_client

    @staticmethod
    def create_github_key(github_key: str) -> str:
        return f"{CachePrefixes.github.value}:{github_key}"

    async def get_record(self, cache_key: str) -> list[GitHubFileContent]:
        cached_record = await self.redis_client.get(
            name=cache_key
        )
        if cached_record is not None:
            return [GitHubFileContent.model_validate(record) for record in loads(cached_record)]

    async def create_record(self, cache_key: str, data: list[dict]):
        await self.redis_client.set(name=cache_key, value=dumps(data), ex=self.cache_ttl)
