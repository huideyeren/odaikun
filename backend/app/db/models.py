from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date, Text
import sqlalchemy.orm

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

    topics = relationship("Topic", backref="user")


class Topic(Base):
    __tablename__ = "topic"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(Text, index=True, nullable=False)
    picture_url = Column(String)
    post_date = Column(Date)
    is_visible = Column(Boolean, default=True)
    is_adopted = Column(Boolean, default=False)
    contributor_id = Column(Integer, ForeignKey("user.id"))
    contributor = relationship("User", foreign_keys=[contributor_id])
