from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.modules.subjects.schemas import SubjectCreate, SubjectResponse, SubjectUpdate
from app.modules.subjects.service import (
    create_subject,
    delete_subject,
    get_owned_subject,
    list_subjects,
    update_subject,
)
from app.modules.users.models import User

router = APIRouter()


@router.get("", response_model=list[SubjectResponse])
def list_subjects_route(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_subjects(db, current_user)


@router.post("", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
def create_subject_route(
    payload: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_subject(db, current_user, payload)


@router.get("/{subject_id}", response_model=SubjectResponse)
def get_subject_route(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_owned_subject(db, current_user, subject_id)


@router.patch("/{subject_id}", response_model=SubjectResponse)
def update_subject_route(
    subject_id: int,
    payload: SubjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_subject(db, current_user, subject_id, payload)


@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subject_route(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    delete_subject(db, current_user, subject_id)
