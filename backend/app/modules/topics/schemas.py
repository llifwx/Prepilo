from datetime import datetime

from pydantic import BaseModel, Field

from app.shared.enums import TopicStatus


class TopicCreate(BaseModel):
    subject_id: int
    title: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=4000)
    difficulty: int = Field(default=3, ge=1, le=5)
    priority: int = Field(default=2, ge=1, le=3)
    estimated_hours: float = Field(default=1.0, ge=0.25, le=100)


class TopicUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=4000)
    difficulty: int | None = Field(default=None, ge=1, le=5)
    priority: int | None = Field(default=None, ge=1, le=3)
    estimated_hours: float | None = Field(default=None, ge=0.25, le=100)
    status: TopicStatus | None = None


class TopicResponse(BaseModel):
    id: int
    subject_id: int
    title: str
    description: str | None
    difficulty: int
    priority: int
    estimated_hours: float
    status: TopicStatus
    created_at: datetime

    model_config = {"from_attributes": True}
