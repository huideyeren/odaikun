from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db import models
from app.db.schemas import users


def get_user(db: Session, user_id: int):
    """
    get_user ユーザー情報を取得する

    Args:
        db (Session): データベース接続
        user_id (int): ユーザーのID

    Raises:
        HTTPException: ユーザーが見つからない旨のHTTP 404 エラー

    Returns:
        schemas.UserBase: ユーザー情報
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_email(db: Session, email: str):
    """
    get_user_by_email 指定したメールアドレスを持つユーザー情報を取得する

    Args:
        db (Session): データベース接続
        email (str): メールアドレス

    Returns:
        schemas.UserBase: [description]
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    get_users 複数のユーザー情報を取得する

    Args:
        db (Session): データベース接続
        skip (int, optional): スキップする件数。デフォルトは0件
        limit (int, optional): 最大件数。デフォルトは100件

    Returns:
        t.List[schemas.UserOut]: ユーザー情報のリスト
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: users.UserCreate):
    """
    create_user ユーザーを作成する

    Args:
        db (Session): データベース接続
        user (schemas.UserCreate): 作成するユーザーの情報

    Returns:
        models.User: 作成されるユーザーの情報
    """
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    """
    delete_user ユーザー情報を削除する

    Args:
        db (Session): データベース接続
        user_id (int): 削除するユーザーのID

    Raises:
        HTTPException: ユーザーが見つからない旨のHTTP 404 エラー

    Returns:
        schemas.UserBase: 削除されるユーザー情報
    """
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return user


def edit_user(db: Session, user_id: int, user: users.UserEdit):
    """
    edit_user ユーザー情報を編集する

    Args:
        db (Session): データベース接続
        user_id (int): 編集するユーザーのID
        user (schemas.UserEdit): 編集するユーザーのデータ

    Raises:
        HTTPException: ユーザーが見つからない旨のHTTP 404 エラー

    Returns:
        schemas.User: 編集されるユーザー情報
    """
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(user.password)
        del update_data["password"]

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
