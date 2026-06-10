from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.subjects.models import Subject
from app.modules.subjects.schemas import SubjectCreate, SubjectUpdate


def get_subject_by_id(db: Session, subject_id: int) -> Subject | None:
    return db.get(Subject, subject_id)


def get_user_subjects(db: Session, user_id: int) -> list[Subject]:
    return list(
        db.scalars(
            select(Subject)
            .where(Subject.owner_id == user_id)
            .order_by(Subject.created_at.desc())
        )
    )


def create_subject(db: Session, user_id: int, payload: SubjectCreate) -> Subject:
    subject = Subject(owner_id=user_id, **payload.model_dump())
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


def update_subject(db: Session, subject: Subject, payload: SubjectUpdate) -> Subject:
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(subject, field, value)
    db.commit()
    db.refresh(subject)
    return subject


def delete_subject(db: Session, subject: Subject) -> None:
    db.delete(subject)
    db.commit()
