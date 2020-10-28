from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from ..session import Base


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
