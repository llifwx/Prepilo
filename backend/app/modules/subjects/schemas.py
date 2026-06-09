from datetime import date, datetime

from pydantic import BaseModel, Field


class SubjectCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=4000)
    exam_date: date | None = None
    color: str | None = Field(default=None, max_length=32)


class SubjectUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=4000)
    exam_date: date | None = None
    color: str | None = Field(default=None, max_length=32)


class SubjectResponse(BaseModel):
    id: int
    owner_id: int
    title: str
    description: str | None
    exam_date: date | None
    color: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
