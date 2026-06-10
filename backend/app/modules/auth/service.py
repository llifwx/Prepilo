from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.modules.auth.schemas import LoginRequest, RegisterRequest, TokenResponse
from app.modules.auth.utils import to_user_create
from app.modules.users import repository
from app.modules.users.service import register_user

_DUMMY_HASH = hash_password("dummy-always-fails-Prepilo$ecure!xk9m")


def register(db: Session, payload: RegisterRequest) -> TokenResponse:
    user = register_user(
        db, to_user_create(payload.username, payload.email, payload.password)
    )
    return TokenResponse(access_token=create_access_token(str(user.id)))


def login(db: Session, payload: LoginRequest) -> TokenResponse:
    user = repository.get_user_by_email(db, payload.login)
    if user is None:
        user = repository.get_user_by_username(db, payload.login)

    candidate_hash = user.hashed_password if user is not None else _DUMMY_HASH
    if user is None or not verify_password(payload.password, candidate_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login or password"
        )

    return TokenResponse(access_token=create_access_token(str(user.id)))
