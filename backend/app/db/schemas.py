from datetime import date
from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    """
    UserBase ユーザーの基礎的な情報

    Args:
        BaseModel (BaseModel): Pydanticでモデルのベースとなるクラス

    Attributes:
        email (str): ユーザーのメールアドレス
        is_active (bool): 有効かどうかを表すフラグ
        is_superuser (bool): 管理者権限があるかどうかを表すフラグ
        first_name (Optional[str]): ユーザーの名
        last_name (Optional[str]): ユーザーの姓
    """
    email: str
    is_active: bool = True
    is_superuser: bool = False
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserOut(UserBase):
    """
    UserOut 出力用のユーザー情報

    Args:
        UserBase (UserBase): ユーザーの基礎的な情報
    """
    pass


class UserCreate(UserBase):
    """
    UserCreate ユーザーを作成するときの情報

    Args:
        UserBase (UserBase): ユーザーの基礎的な情報

    Attributes:
        password (str): パスワード
    """
    password: str

    class Config:
        """
        UserCreateクラスの設定

        Attributes:
            orm_mode (bool): ORMモードか
        """
        orm_mode = True


class UserEdit(UserBase):
    """
    UserEdit ユーザーを編集するときの情報

    Args:
        UserBase (UserBase): ユーザーの基礎的な情報

    Attributes:
        password (t.Optional[str]): パスワード
    """
    password: str

    class Config:
        """
        UserEditクラスの設定

        Attributes:
            orm_mode (bool): ORMモードか
        """
        orm_mode = True


class User(UserBase):
    """
    User ユーザーの情報

    Args:
        UserBase (UserBase): ユーザーの基礎的な情報
    
    Attributes:
        id (int): ユーザーID
    """    
    id: int

    class Config:
        """
        Userクラスの設定

        Attributes:
            orm_mode (bool): ORMモードか
        """
        orm_mode = True


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


class TopicBase(BaseModel):
    topic: str
    picture_url: Optional[str] = None
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

