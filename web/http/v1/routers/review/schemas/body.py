from enum import StrEnum
from typing import Annotated

from pydantic import Field, HttpUrl

from web.http.v1.schemas.base import BaseAPISchema


class CandidateLevels(StrEnum):
    junior = "Junior"
    middle = "Middle"
    senior = "Senior"


class ReviewBody(BaseAPISchema):
    assignment_description: Annotated[str, Field(min_length=12)]

    github_repo_url: Annotated[HttpUrl, Field()]
    candidate_level: Annotated[CandidateLevels, Field()]
