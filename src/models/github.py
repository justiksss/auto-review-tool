from typing import Annotated

from pydantic import Field

from src.models.base import BaseEntityModel


class GitHubFileContent(BaseEntityModel):
    file_path: Annotated[str, Field()]
    file_content: Annotated[str, Field()]

    file_name: Annotated[str, Field()]
