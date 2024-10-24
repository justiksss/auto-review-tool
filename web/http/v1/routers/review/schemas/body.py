from enum import StrEnum
from typing import Annotated

from fastapi import HTTPException
from pydantic import Field, HttpUrl, field_validator

from web.http.v1.schemas.base import BaseAPISchema


class CandidateLevels(StrEnum):
    junior = "Junior"
    middle = "Middle"
    senior = "Senior"


class ReviewBody(BaseAPISchema):
    assignment_description: Annotated[str, Field(min_length=12)]

    github_repo_url: Annotated[HttpUrl, Field()]
    candidate_level: Annotated[CandidateLevels, Field()]

    @field_validator('github_repo_url')
    def validate_github_repo_url(cls, value: HttpUrl) -> HttpUrl:
        if not value.host.startswith('https://github.com/'):
            raise HTTPException(status_code=422, detail='Github repo url must start with "https://github.com/"')
            # replace on own exception

        return value
