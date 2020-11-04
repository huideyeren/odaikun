import typing as t

from fastapi import APIRouter, Depends, Request, Response

from app.core.auth import get_current_active_user
from app.db.crud.topic_crud import (
    create_topic,
    drop_topic,
    edit_topic,
    get_topics,
    get_topic,
)
from app.db.schemas.topics import Topic, TopicCreate, TopicEdit
from app.db.session import get_db

topics_router = r = APIRouter()


@r.get(
    "/topics",
    response_model=t.List[Topic],
    response_model_exclude_none=True,
)
async def topics_list(response: Response, db=Depends(get_db)):
    topics = get_topics(db)
    return topics


@r.get(
    "/topics/{topic_id}",
    response_model=Topic,
    response_model_exclude_none=True,
)
async def topic_details(
    request: Request,
    topic_id: int,
    db=Depends(get_db),
):
    topic = get_topic(db, topic_id)
    return topic


@r.post("/topics", response_model=Topic, response_model_exclude_none=True)
async def topic_create(
    request: Request,
    topic: TopicCreate,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return create_topic(db, topic, current_user)


@r.put("/topics/{topic_id}", response_model=Topic, response_model_exclude_none=True)
async def topic_edit(
    request: Request,
    topic_id: int,
    topic: TopicEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return edit_topic(db, topic_id, topic, current_user)


@r.delete("/topics/{topic_id}", response_model=Topic, response_model_exclude_none=True)
async def topic_delete(
    request: Request,
    topic_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return drop_topic(db, topic_id, current_user)
