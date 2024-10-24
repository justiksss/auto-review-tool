from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis

from settings import Settings
from web.http.v1.dependecies.settings import get_api_settings


async def get_redis_client(
    settings: Annotated[Settings, Depends(get_api_settings)],
) -> Redis:
    return Redis(host=settings.REDIS_HOST, port=int(settings.REDIS_PORT), decode_responses=True)
