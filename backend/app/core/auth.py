from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from jwt import PyJWTError

from app.core import security
from app.db import models, session
from app.db.crud.user_crud import create_user, get_user_by_email
from app.db.schemas import tokens, users


async def get_current_user(
    db=Depends(session.get_db), token: str = Depends(security.oauth2_scheme)
):
    """
    get_current_user 現在のユーザーを取得する

    Args:
        db (Any, optional): DB接続。初期値は Depends(session.get_db)。
        token (str, optional): JWTトークン。初期値は Depends(security.oauth2_scheme)。

    Raises:
        credentials_exception: 認証キーが正しくないことを表す HTTP 401 エラー。

    Returns:
        Any: ユーザー情報
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        email: Optional[str] = payload.get("sub")
        if email is None:
            raise credentials_exception
        permissions: Optional[str] = payload.get("permissions")
        if permissions is None:
            raise credentials_exception
        token_data = tokens.TokenData(email=email, permissions=permissions)
    except PyJWTError:
        raise credentials_exception
    user = get_user_by_email(db, str(token_data.email))
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
):
    """
    get_current_active_user 活動できるユーザーを取得する。

    Args:
        current_user (models.User, optional):
            現在のユーザー。初期値は Depends(get_current_user)。

    Raises:
        HTTPException: このユーザーが活動できない状態を表す HTTP 400 エラー。

    Returns:
        User: 現在のユーザー
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """
    get_current_active_superuser 活動できる管理者ユーザーを取得する。

    Args:
        current_user (models.User, optional):
            現在のユーザー。初期値は Depends(get_current_user)。

    Raises:
        HTTPException: 権限が無いことを表す HTTP 403 エラー。

    Returns:
        models.User: 現在のユーザー。
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


def authenticate_user(db, email: str, password: str):
    """
    authenticate_user ユーザー認証を行う

    Args:
        db (Any): DB接続
        email (str): Eメールアドレス
        password (str): パスワード

    Returns:
        Any: ユーザー情報（無い場合はFalse）
    """
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not security.verify_password(password, user.hashed_password):
        return False
    return user


def sign_up_new_user(db, email: str, password: str):
    """
    sign_up_new_user ユーザーのサインアップ

    Args:
        db (Any): DB接続
        email (str): Eメールアドレス
        password (str): パスワード

    Returns:
        User: 新しいユーザー
    """
    user = get_user_by_email(db, email)
    if user:
        return False  # User already exists
    new_user = create_user(
        db,
        users.UserCreate(
            email=email,
            password=password,
            is_active=True,
            is_superuser=False,
        ),
    )
    return new_user
