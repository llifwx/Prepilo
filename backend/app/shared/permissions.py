from app.modules.subjects.models import Subject
from app.modules.users.models import User


def owns_subject(user: User, subject: Subject) -> bool:
    return subject.owner_id == user.id
