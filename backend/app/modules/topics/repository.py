from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.modules.topics.models import Topic
from app.modules.topics.schemas import TopicCreate, TopicUpdate


def get_topic_by_id(db: Session, topic_id: int) -> Topic | None:
    return db.scalar(
        select(Topic).options(joinedload(Topic.subject)).where(Topic.id == topic_id)
    )


def get_subject_topics(db: Session, subject_id: int) -> list[Topic]:
    return list(
        db.scalars(
            select(Topic)
            .where(Topic.subject_id == subject_id)
            .order_by(Topic.created_at.desc())
        )
    )


def create_topic(db: Session, payload: TopicCreate) -> Topic:
    topic = Topic(**payload.model_dump())
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic


def update_topic(db: Session, topic: Topic, payload: TopicUpdate) -> Topic:
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(topic, field, value)
    db.commit()
    db.refresh(topic)
    return topic


def delete_topic(db: Session, topic: Topic) -> None:
    db.delete(topic)
    db.commit()
