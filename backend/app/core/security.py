from datetime import datetime, timedelta

import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "super_secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_password_hash(password: str) -> str:
    """
    get_password_hash パスワードのハッシュを取得する

    Args:
        password (str): パスワード

    Returns:
        str: ハッシュ化されたパスワード
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    verify_password パスワードが正しいか判定する

    Args:
        plain_password (str): 平文のパスワード
        hashed_password (str): ハッシュ化されたパスワード

    Returns:
        bool: パスワードが正しいか否か
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    """
    create_access_token アクセストークンの生成

    Args:
        data (dict): データ
        expires_delta (timedelta, optional): （不明）。初期値は None。

    Returns:
        [type]: [description]
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
