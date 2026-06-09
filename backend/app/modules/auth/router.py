from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.schemas import LoginRequest, RegisterRequest, TokenResponse
from app.modules.auth.service import login, register

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=201)
def register_route(payload: RegisterRequest, db: Session = Depends(get_db)) -> TokenResponse:
    return register(db, payload)


@router.post("/login", response_model=TokenResponse)
def login_route(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    return login(db, payload)
