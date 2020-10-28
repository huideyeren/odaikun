from datetime import date
from typing import Optional

from pydantic import BaseModel, HttpUrl

from app.db.schemas.users import User


class TopicBase(BaseModel):
    topic: str
    picture_url: Optional[HttpUrl] = None
    post_date: date
    is_visible: bool = True
    is_adopted: bool = False
    contributor_id: int


class TopicOut(TopicBase):
    contributor: User


class TopicCreate(TopicBase):
    class Config:
        orm_mode = True


class TopicEdit(TopicBase):
    class Config:
        orm_mode = True


class Topic(TopicBase):
    id: int

    class Config:
        orm_mode = True
