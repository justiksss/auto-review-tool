from typing import Annotated

from pydantic import Field

from src.models.base import BaseEntityModel


class OpenAIResultEntity(BaseEntityModel):
    rating: Annotated[str | None, Field()] = None
    conclusion: Annotated[str | None, Field()] = None
