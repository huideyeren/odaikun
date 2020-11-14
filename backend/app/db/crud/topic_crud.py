import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db import models
from app.db.schemas import topics, users


def get_topic(db: Session, topic_id: int):
    """
    get_topic 指定されたIDのお題を取得する

    Args:
        db (Session): DB接続
        topic_id (int): お題のID

    Raises:
        HTTPException: お題が見つからない旨のHTTP 404 エラー

    Returns:
        Topic: 指定されたIDのお題
    """
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


def get_topics(db: Session):
    """
    get_topics 見える状態のお題一覧を取得する

    Args:
        db (Session): DB接続

    Returns:
        Any: 見える状態のお題一覧
    """
    return db.query(models.Topic).filter(models.Topic.is_visible).all()


def get_all_topics(db: Session):
    """
    get_all_topics 全てのお題一覧を取得する

    Args:
        db (Session): DB接続

    Returns:
        Any: 全てのお題一覧
    """
    return db.query(models.Topic).all()


def get_topics_by_user(db: Session, user_id: int):
    """
    get_topics_by_user 指定したIDのユーザーが作成した未削除のお題一覧を取得する

    Args:
        db (Session): DB接続
        user_id (int): ユーザーID

    Returns:
        Any: 指定したユーザーIDのユーザーが作成したお題一覧
    """
    return (
        db.query(models.Topic)
        .filter(models.Topic.is_visible)
        .filter(models.Topic.contributor_id == user_id)
        .all()
    )


def get_all_topics_by_user(db: Session, user_id: int):
    """
    get_all_topics_by_user 指定したIDのユーザーが作成した全てのお題を取得する

    Args:
        db (Session): DB接続
        user_id (int): ユーザーID

    Returns:
        Any: 指定したIDのユーザーが作成した全てのお題
    """
    return db.query(models.Topic).filter(models.Topic.contributor_id == user_id).all()


def get_adopted_topics(db: Session):
    """
    get_adopted_topics 採用済みのお題一覧を取得する

    Args:
        db (Session): DB接続

    Returns:
        Any: 採用済みのお題一覧
    """
    return (
        db.query(models.Topic)
        .filter(models.Topic.is_visible)
        .filter(models.Topic.is_adopted)
        .all()
    )


def get_adopted_topics_by_user(db: Session, user_id: int):
    """
    get_adopted_topics_by_user 指定したIDのユーザーが作成した採用済みのお題を取得する

    Args:
        db (Session): DB接続
        user_id (int): ユーザーID

    Returns:
        Any: 指定したIDのユーザーが作成した採用済みのお題
    """
    return (
        db.query(models.Topic)
        .filter(models.Topic.is_visible)
        .filter(models.Topic.contributor_id == user_id)
        .filter(models.Topic.is_adopted)
        .all()
    )


def get_topics_by_keyword(db: Session, keyword: str):
    """
    get_topics_by_keyword 指定したキーワードを含む未削除のお題一覧を取得する

    Args:
        db (Session): DB接続
        keyword (str): キーワード

    Returns:
        Any: 指定したキーワードを含むお題一覧
    """
    return (
        db.query(models.Topic)
        .filter(models.Topic.is_visible)
        .filter(models.Topic.topic.like("%\\" + keyword + "%", escape="\\"))
        .all()
    )


def get_all_topics_by_keyword(db: Session, keyword: str):
    """
    get_all_topics_by_keyword 指定したキーワードを含む全てのお題一覧を取得する

    Args:
        db (Session): DB接続
        keyword (str): 指定したキーワードを含む全てのお題一覧

    Returns:
        Any: 指定したキーワードを含む全てのお題一覧
    """
    return (
        db.query(models.Topic)
        .filter(models.Topic.topic.like("%\\" + keyword + "%", escape="\\"))
        .all()
    )


def create_topic(db: Session, topic: topics.TopicCreate, current_user: users.User):
    """
    create_topic お題を投稿する

    Args:
        db (Session): DB接続
        topic (topics.TopicCreate): お題
        current_user (users.User): 現在ログインしているユーザーの情報

    Raises:
        HTTPException: 認証していない旨の HTTP 401 エラー

    Returns:
        Topic: 作成されたお題
    """
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
    """
    edit_topic お題を編集する

    Args:
        db (Session): DB接続
        topic_id (int): お題のID
        topic (topics.TopicEdit): 編集されたお題
        current_user (users.User): 現在ログインしているユーザーの情報

    Raises:
        HTTPException: 認証していない旨の HTTP 401 エラー
        HTTPException: お題の投稿者でない旨の HTTP 403 エラー
        HTTPException: 指定されたIDのお題が無い旨の HTTP 404 エラー

    Returns:
        Any: 編集されたお題
    """
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
    """
    drop_topic お題を削除する

    Args:
        db (Session): DB接続
        topic_id (int): お題のID
        current_user (users.User): 現在ログインしているユーザーの情報

    Raises:
        HTTPException: 認証していない旨の HTTP 401 エラー
        HTTPException: 権限が無い旨の HTTP 403 エラー
        HTTPException: 指定されたIDのお題が無い旨の HTTP 404 エラー

    Returns:
        Any: 削除されたお題
    """
    if not current_user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Login required")
    topic = get_topic(db, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    if current_user.id is not topic.contributor_id and not current_user.is_superuser:
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
