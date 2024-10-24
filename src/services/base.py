from typing import Any

from httpx import AsyncClient
from orjson import loads

from src.interfaces.httpx import AsyncHTTPClient


class BaseService:
    pass


class BaseIntegrationService(AsyncHTTPClient):
    """Base service for external tools"""

    async def get(self, uri: str) -> dict[str, Any]:
        response = await self.async_client.get(
            url=uri
        )

        if response.status_code != 200:
            raise Exception  # raise network exception

        return loads(response.content)
