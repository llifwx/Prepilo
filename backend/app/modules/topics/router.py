from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.modules.topics.schemas import TopicCreate, TopicResponse, TopicUpdate
from app.modules.topics.service import (
    create_topic,
    delete_topic,
    get_owned_topic,
    list_topics_for_subject,
    update_topic,
)
from app.modules.users.models import User

router = APIRouter()


@router.get("", response_model=list[TopicResponse])
def list_topics_route(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_topics_for_subject(db, current_user, subject_id)


@router.post("", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
def create_topic_route(
    payload: TopicCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_topic(db, current_user, payload)


@router.get("/{topic_id}", response_model=TopicResponse)
def get_topic_route(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_owned_topic(db, current_user, topic_id)


@router.patch("/{topic_id}", response_model=TopicResponse)
def update_topic_route(
    topic_id: int,
    payload: TopicUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_topic(db, current_user, topic_id, payload)


@router.delete("/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_topic_route(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    delete_topic(db, current_user, topic_id)
