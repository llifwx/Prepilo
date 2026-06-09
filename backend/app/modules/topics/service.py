from sqlalchemy.orm import Session

from app.core.exceptions import forbidden, not_found
from app.modules.subjects.service import get_owned_subject
from app.modules.topics import repository
from app.modules.topics.models import Topic
from app.modules.topics.schemas import TopicCreate, TopicUpdate
from app.modules.users.models import User


def list_topics_for_subject(db: Session, user: User, subject_id: int) -> list[Topic]:
    get_owned_subject(db, user, subject_id)
    return repository.get_subject_topics(db, subject_id)


def get_owned_topic(db: Session, user: User, topic_id: int) -> Topic:
    topic = repository.get_topic_by_id(db, topic_id)
    if topic is None:
        raise not_found("Topic not found")
    if topic.subject.owner_id != user.id:
        raise forbidden("You can only access topics from your own subjects")
    return topic


def create_topic(db: Session, user: User, payload: TopicCreate) -> Topic:
    get_owned_subject(db, user, payload.subject_id)
    return repository.create_topic(db, payload)


def update_topic(db: Session, user: User, topic_id: int, payload: TopicUpdate) -> Topic:
    topic = get_owned_topic(db, user, topic_id)
    return repository.update_topic(db, topic, payload)


def delete_topic(db: Session, user: User, topic_id: int) -> None:
    topic = get_owned_topic(db, user, topic_id)
    repository.delete_topic(db, topic)
