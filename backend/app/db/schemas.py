from pydantic import BaseModel
import typing as t


class UserBase(BaseModel):
    """
    UserBase ユーザーの基礎的な情報

    Args:
        BaseModel ([type]): [description]

    Attributes:
        email (str): ユーザーのメールアドレス
        is_active (bool): 有効かどうかを表すフラグ
        is_superuser (bool): 管理者権限があるかどうかを表すフラグ
        first_name (str): ユーザーの名
        last_name (str): ユーザーの姓
    """
    email: str
    is_active: bool = True
    is_superuser: bool = False
    first_name: str = None
    last_name: str = None


class UserOut(UserBase):
    """
    UserOut 出力用のユーザー情報

    Args:
        UserBase (UserBase): ユーザーの基礎的な情報
    """
    pass


class UserCreate(UserBase):
    
    password: str

    class Config:
        orm_mode = True


class UserEdit(UserBase):
    password: t.Optional[str] = None

    class Config:
        orm_mode = True


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    permissions: str = "user"
