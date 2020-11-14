from datetime import date
from typing import Optional

from pydantic import BaseModel, HttpUrl

from app.db.schemas.users import User


class TopicBase(BaseModel):
    """
    TopicBase お題に関する最低限の情報を表すクラス

    Args:
        BaseModel (BaseModel): Pydanticでモデルのベースとなるクラス

    Attributes:
        topic (str): お題の本文。
        picture_url (Optional[HttpUrl]): お題の説明となる画像のURL。無くても良い。
        post_date (date): 投稿日。
        is_visible (bool): 見える状態（未削除）かを表すフラグ。デフォルトはTrue。
        is_adopted (bool): 採用済みかを表すフラグ。デフォルトはFalse。
        contributor_id (int): 投稿者のID。
    """

    topic: str
    picture_url: Optional[HttpUrl] = None
    post_date: date
    is_visible: bool = True
    is_adopted: bool = False
    contributor_id: int


class TopicOut(TopicBase):
    """
    TopicOut お題に関する出力用の情報を表すクラス

    Args:
        TopicBase (TopicBase): お題に関する最低限の情報を表すクラス

    Attributes:
        contributor (User): 投稿者情報を格納するクラス
    """

    contributor: User


class TopicCreate(TopicBase):
    """
    TopicCreate お題を投稿する際に情報を格納するクラス

    Args:
        TopicBase (TopicBase): お題に関する最低限の情報を表すクラス
    """

    class Config:
        """
        TopicCreate.Config TopicCreateクラスの設定

        Attributes:
            orm_mode (bool): ORMモードか
        """

        orm_mode = True


class TopicEdit(TopicBase):
    """
    TopicEdit お題を編集する際に情報を格納するクラス

    Args:
        TopicBase (TopicBase): お題に関する最低限の情報を表すクラス
    """

    class Config:
        """
        TopicEdit.Config TopicCreateクラスの設定

        Attributes:
            orm_mode (bool): ORMモードか
        """

        orm_mode = True


class Topic(TopicBase):
    """
    Topic お題に関する情報を表すクラス

    Args:
        TopicBase (TopicBase): お題に関する最低限の情報を表すクラス
    """

    id: int

    class Config:
        """
        Topic.Config Topicクラスの設定

        Attributes:
            orm_mode (bool): ORMモードか
        """

        orm_mode = True
