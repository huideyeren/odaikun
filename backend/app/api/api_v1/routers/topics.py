from fastapi import APIRouter, Request, Depends, Response
import typing as t

from app.db import models, schemas
from app.db.session import get_db
from app.db.crud import get_topics, create_topic, drop_topic, edit_topic
from app.core.auth import get_current_active_user

topics_router = r = APIRouter()


@r.get(
    "/topics",
    response_model=t.List[models.Topic],
    response_model_exclude_none=True,
)
async def topics_list(response: Response, db=Depends(get_db)):
    topics = get_topics(db)
    return topics


@r.post("/topics", response_model=models.Topic, response_model_exclude_none=True)
async def topic_create(
    request: Request,
    topic: schemas.TopicCreate,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return create_topic(db, topic, current_user)


@r.put("/topics/{topic_id}", response_model=models.Topic, response_model_exclude_none=True)
async def topic_edit(
    request: Request,
    topic_id: int,
    topic: schemas.TopicEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return edit_topic(db, topic_id, topic, current_user)


@r.delete("/topics/{topic_id}", response_model=models.Topic, response_model_exclude_none=True)
async def topic_delete(
    request: Request,
    topic_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return drop_topic(db, topic_id, current_user)
