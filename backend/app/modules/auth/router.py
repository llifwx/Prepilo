from fastapi import APIRouter, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.schemas import LoginRequest, RegisterRequest, TokenResponse
from app.modules.auth.service import login, register

router = APIRouter()
_limiter = Limiter(key_func=get_remote_address)


@router.post("/register", response_model=TokenResponse, status_code=201)
@_limiter.limit("10/minute")
def register_route(request: Request, payload: RegisterRequest, db: Session = Depends(get_db)) -> TokenResponse:
    return register(db, payload)


@router.post("/login", response_model=TokenResponse)
@_limiter.limit("5/minute")
def login_route(request: Request, payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    return login(db, payload)
