from sqlalchemy import Boolean, Column, Integer, String

from .session import Base


class User(Base):
    """
    User

    Userテーブルに対応するDBモデル

    Args:
        Base ([type]): [description]

    Attributes:
        id (int): ユーザーID
        email (str): ユーザーのメールアドレス
        first_name (str): ユーザーの名
        last_name (str): ユーザーの姓
        hashed_password (str): ハッシュ化されたパスワード文字列
        is_active (bool): 有効かどうかを表すフラグ
        is_superuser (bool): 管理者権限があるかどうかを表すフラグ
    """

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
