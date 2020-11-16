from app.core.celery_app import celery_app


@celery_app.task(acks_late=True)
def example_task(word: str) -> str:
    """
    example_task サンプルタスク

    Args:
        word (str): 返したい単語

    Returns:
        str: テストタスクが返す文字列
    """
    return f"test task returns {word}"
