import typing as t

from fastapi import APIRouter, Depends, Request, Response

from app.core.auth import get_current_active_user
from app.db.crud.topic_crud import (
    create_topic,
    drop_topic,
    edit_topic,
    get_topic,
    get_topics,
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
    """
    topics_list GETでリクエストを送るとお題リストを取得する。

    Args:
        response (Response): レスポンス
        db (Any, optional): DB接続。初期値はDepends(get_db)。

    Returns:
        Any: 現在見える状態のお題のリスト
    """
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
    """
    topic_details IDを指定してGETでリクエストを送ると指定されたIDのお題の詳細を取得する。

    Args:
        request (Request): リクエスト
        topic_id (int): お題のID
        db (Any, optional): DB接続。初期値はDepends(get_db)。

    Returns:
        Any: 指定されたIDのお題
    """
    topic = get_topic(db, topic_id)
    return topic


@r.post("/topics", response_model=Topic, response_model_exclude_none=True)
async def topic_create(
    request: Request,
    topic: TopicCreate,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    topic_create POSTでリクエストを送るとお題を投稿する。

    Args:
        request (Request): リクエスト
        topic (TopicCreate): 投稿するお題
        db (Any, optional): DB接続。初期値はDepends(get_db)。
        current_user (Any, optional):
            現在のユーザー。初期値はDepends(get_current_active_user)。

    Returns:
        Topic: 作成されたお題
    """
    return create_topic(db, topic, current_user)


@r.put("/topics/{topic_id}", response_model=Topic, response_model_exclude_none=True)
async def topic_edit(
    request: Request,
    topic_id: int,
    topic: TopicEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    topic_edit IDを指定してPUTでリクエストを送ると指定されたIDのお題をアップデートする。

    Args:
        request (Request): リクエスト
        topic_id (int): アップデートするお題のID
        topic (TopicEdit): アップデートするお題の内容
        db (Any, optional): DB接続。初期値はDepends(get_db)。
        current_user (Any, optional):
            現在のユーザー。初期値はDepends(get_current_active_user)。

    Returns:
        Any: アップデートされたお題
    """
    return edit_topic(db, topic_id, topic, current_user)


@r.delete("/topics/{topic_id}", response_model=Topic, response_model_exclude_none=True)
async def topic_delete(
    request: Request,
    topic_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    topic_delete IDを指定してDELETEでリクエストを送ると指定されたIDのお題を削除する。

    Args:
        request (Request): リクエスト
        topic_id (int): お題のID
        db (Any, optional): DB接続。初期値はDepends(get_db)。
        current_user (Any, optional):
            現在のユーザー。初期値はDepends(get_current_active_user)。

    Returns:
        Any: 削除されたお題
    """
    return drop_topic(db, topic_id, current_user)
