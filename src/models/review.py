from typing import Annotated

from pydantic import Field

from src.models.base import BaseEntityModel
from src.models.github import GitHubFileContent


class ReviewResponseEntityModel(BaseEntityModel):
    found_files: Annotated[list[GitHubFileContent] | None, Field()] = None
    comments: Annotated[str | None, Field()] = None

    rating: Annotated[str | None, Field()] = None
    conclusion: Annotated[str | None, Field()] = None
