from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date, Text

from .session import Base


class User(Base):
    """
    User userテーブルのテーブル定義

    Args:
        Base (Type[__class_DeclarativeMeta]): テーブルのメタデータ
    """

    __tablename__ = "user"  #: テーブルの名前

    id = Column(Integer, primary_key=True, index=True)  #: ID
    email = Column(String, unique=True, index=True, nullable=False)  #: メールアドレス
    first_name = Column(String)  #: 名
    last_name = Column(String)  #: 姓
    hashed_password = Column(String, nullable=False)  #: ハッシュ化されたパスワード
    is_active = Column(Boolean, default=True)  #: アクティブな状態か？
    is_superuser = Column(Boolean, default=False)  #: スーパーユーザーか？

    topics = relationship("Topic", backref="user")  #: topicテーブルとのリレーション


class Topic(Base):
    """
    Topic topicテーブルのテーブル定義

    Args:
        Base (Type[__class_DeclarativeMeta]): テーブルのメタデータ
    """

    __tablename__ = "topic"  #: テーブルの名前

    id = Column(Integer, primary_key=True, index=True)  #: ID
    topic = Column(Text, index=True, nullable=False)  #: お題本文
    picture_url = Column(String)  #: 画像のURL
    post_date = Column(Date)  #: 投稿日
    is_visible = Column(Boolean, default=True)  #: 表示できる状態になっているか？
    is_adopted = Column(Boolean, default=False)  #: 採用されたか？
    contributor_id = Column(Integer, ForeignKey("user.id"))  #: 投稿者のユーザーID
    contributor = relationship(
        "User", foreign_keys=[contributor_id]
    )  #: userテーブルとのリレーション
