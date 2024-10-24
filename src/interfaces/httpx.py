from dataclasses import dataclass
from typing import Self

from httpx import AsyncClient


@dataclass
class HttpxConfig:
    base_url: str


class AsyncHTTPClient:
    def __init__(self, config: HttpxConfig) -> None:
        self.async_client = AsyncClient(
            base_url=config.base_url
        )

    def _set_headers(self, **headers) -> None:
        assert self.async_client

        self.async_client.headers.update(headers)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Handle exceptions if exists"""
        await self.async_client.aclose()
