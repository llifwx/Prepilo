from app.modules.users.schemas import UserCreate


def to_user_create(username: str, email: str, password: str) -> UserCreate:
    return UserCreate(username=username, email=email, password=password)
