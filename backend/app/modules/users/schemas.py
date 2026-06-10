from datetime import datetime

from pydantic import AnyHttpUrl, BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    avatar: AnyHttpUrl | None = None
    bio: str | None = Field(default=None, max_length=1000)
    daily_study_goal_hours: float | None = Field(default=None, ge=0.5, le=12)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    avatar: str | None
    bio: str | None
    daily_study_goal_hours: float
    created_at: datetime

    model_config = {"from_attributes": True}
