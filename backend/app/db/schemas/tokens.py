from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """
    Token JWTトークン

    Args:
        BaseModel (BaseModel): Pydanticでモデルのベースとなるクラス

    Attributes:
        access_token (str): アクセストークン本体
        token_type (str): アクセストークンの型情報
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    TokenData JWTトークンに格納するデータ

    Args:
        BaseModel (BaseModel): Pydanticでモデルのベースとなるクラス

    Attributes:
        email (Optional[str]): メールアドレス
        permissions (str): 権限を表す文字列
    """

    email: Optional[str] = None
    permissions: str = "user"
