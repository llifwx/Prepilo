import re
from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator

_HEX_COLOR_RE = re.compile(r'^#[0-9A-Fa-f]{3,8}$')


def _validate_color(v: str | None) -> str | None:
    if v is not None and not _HEX_COLOR_RE.match(v):
        raise ValueError("color must be a valid hex color code (e.g. #FF5733)")
    return v


class SubjectCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=4000)
    exam_date: date | None = None
    color: str | None = Field(default=None, max_length=32)

    @field_validator("color")
    @classmethod
    def color_must_be_hex(cls, v: str | None) -> str | None:
        return _validate_color(v)


class SubjectUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=4000)
    exam_date: date | None = None
    color: str | None = Field(default=None, max_length=32)

    @field_validator("color")
    @classmethod
    def color_must_be_hex(cls, v: str | None) -> str | None:
        return _validate_color(v)


class SubjectResponse(BaseModel):
    id: int
    title: str
    description: str | None
    exam_date: date | None
    color: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
