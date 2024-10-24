from typing import ClassVar

from pydantic import BaseModel, ConfigDict


class BaseAPISchema(BaseModel):
    """Base model fo all API schemas."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        from_attributes=True, arbitrary_types_allowed=True, extra="forbid"
    )
