import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db import models
from app.db.schemas import topics, users


def get_topic(db: Session, topic_id: int):
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


def get_topics(db: Session):
    return db.query(models.Topic).filter(models.Topic.is_visible).all()


def get_all_topics(db: Session):
    return db.query(models.Topic).all()


def get_topics_by_user(db: Session, user_id: int):
    return (
        db.query(models.Topic)
        .filter(models.Topic.is_visible)
        .filter(models.Topic.contributor_id == user_id)
        .all()
    )


def get_all_topics_by_user(db: Session, user_id: int):
    return db.query(models.Topic).filter(models.Topic.contributor_id == user_id).all()


def get_adopted_topics(db: Session):
    return (
        db.query(models.Topic)
        .filter(models.Topic.is_visible)
        .filter(models.Topic.is_adopted)
        .all()
    )


def get_adopted_topics_by_user(db: Session, user_id: int):
    return (
        db.query(models.Topic)
        .filter(models.Topic.is_visible)
        .filter(models.Topic.contributor_id == user_id)
        .filter(models.Topic.is_adopted)
        .all()
    )


def get_topics_by_keyword(db: Session, keyword: str):
    return (
        db.query(models.Topic)
        .filter(models.Topic.is_visible)
        .filter(models.Topic.topic.like("%\\" + keyword + "%", escape="\\"))
        .all()
    )


def get_all_topics_by_keyword(db: Session, keyword: str):
    return (
        db.query(models.Topic)
        .filter(models.Topic.topic.like("%\\" + keyword + "%", escape="\\"))
        .all()
    )


def create_topic(db: Session, topic: topics.TopicCreate, current_user: users.User):
    if not current_user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Login required")
    topic.contributor_id = current_user.id
    db_topic = models.Topic(
        topic=topic.topic,
        picture_url=topic.picture_url,
        post_date=datetime.date.today(),
        contributor_id=topic.contributor_id,
    )
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic


def edit_topic(
    db: Session, topic_id: int, topic: topics.TopicEdit, current_user: users.User
):
    if not current_user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Login required")
    if current_user.id != topic.contributor_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="You are not contributor")
    db_topic = get_topic(db, topic_id)
    if not db_topic:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Topic not found")
    update_data = topic.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_topic, key, value)

    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic


def drop_topic(db: Session, topic_id: int, current_user: users.User):
    if not current_user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Login required")
    topic = get_topic(db, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    if current_user.id != topic.contributor_id and not current_user.is_superuser:
        print(current_user.id)
        print(topic.contributor_id)
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail="You don't have permission"
        )
    setattr(topic, "is_visible", False)
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic
