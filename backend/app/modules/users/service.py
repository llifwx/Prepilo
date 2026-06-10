from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.users import repository
from app.modules.users.models import User
from app.modules.users.schemas import UserCreate, UserUpdate


def register_user(db: Session, payload: UserCreate) -> User:
    if repository.get_user_by_email(
        db, payload.email
    ) or repository.get_user_by_username(db, payload.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with these details already exists",
        )

    return repository.create_user(db, payload, hash_password(payload.password))


def update_profile(db: Session, user: User, payload: UserUpdate) -> User:
    return repository.update_user(db, user, payload)
