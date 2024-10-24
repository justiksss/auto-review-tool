from typing import Annotated

from pydantic import Field

from src.models.base import BaseEntityModel


class FoundFile(BaseEntityModel):
    file_path: Annotated[str, Field()]
    file_name: Annotated[str, Field()]


class ReviewResponseEntityModel(BaseEntityModel):
    found_files: Annotated[list[FoundFile] | None, Field()] = None
    comments: Annotated[str | None, Field()] = None

    rating: Annotated[str | None, Field()] = None
    conclusion: Annotated[str | None, Field()] = None
