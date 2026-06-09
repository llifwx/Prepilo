from sqlalchemy.orm import Session

from app.core.exceptions import forbidden, not_found
from app.modules.subjects import repository
from app.modules.subjects.models import Subject
from app.modules.subjects.schemas import SubjectCreate, SubjectUpdate
from app.modules.users.models import User


def list_subjects(db: Session, user: User) -> list[Subject]:
    return repository.get_user_subjects(db, user.id)


def get_owned_subject(db: Session, user: User, subject_id: int) -> Subject:
    subject = repository.get_subject_by_id(db, subject_id)
    if subject is None:
        raise not_found("Subject not found")
    if subject.owner_id != user.id:
        raise forbidden("You can only access your own subjects")
    return subject


def create_subject(db: Session, user: User, payload: SubjectCreate) -> Subject:
    return repository.create_subject(db, user.id, payload)


def update_subject(db: Session, user: User, subject_id: int, payload: SubjectUpdate) -> Subject:
    subject = get_owned_subject(db, user, subject_id)
    return repository.update_subject(db, subject, payload)


def delete_subject(db: Session, user: User, subject_id: int) -> None:
    subject = get_owned_subject(db, user, subject_id)
    repository.delete_subject(db, subject)
