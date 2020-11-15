from app.db import models


def test_get_topics(client, test_topic, user_token_headers):
    """
    test_get_topics お題一覧を取得するテスト

    Args:
        client (Any): HTTPクライアント
        test_topic (Any): テスト用お題
        user_token_headers (Any): テスト用一般ユーザーの認証用JWTトークンヘッダー
    """
    response = client.get("/api/v1/topics", headers=user_token_headers)
    assert response.status_code == 200
    assert response.json() == [
        {
            "topic": test_topic.topic,
            "picture_url": test_topic.picture_url,
            "post_date": str(test_topic.post_date),
            "is_visible": test_topic.is_visible,
            "is_adopted": test_topic.is_adopted,
            "contributor_id": test_topic.contributor_id,
            "id": test_topic.id,
        }
    ]


def test_delete_topic(client, test_topic, test_db, user_token_headers):
    """
    test_delete_topic お題の作成者がお題を削除するテスト

    Args:
        client (Any): HTTPクライアント
        test_topic (Any): テスト用お題
        test_db (Any): テスト用DB接続
        user_token_headers (Any): テスト用一般ユーザーの認証用JWTトークンヘッダー
    """
    response = client.delete(
        f"/api/v1/topics/{test_topic.id}", headers=user_token_headers
    )
    assert response.status_code == 200
    assert test_db.query(models.Topic).filter(not models.Topic.is_visible).all() == []


def test_delete_topic_on_superuser(
    client, test_topic_written_by_superuser, test_db, superuser_token_headers
):
    """
    test_delete_topic_on_superuser 管理者が作成したお題を管理者が削除するテスト

    Args:
        client (Any): HTTPクライアント
        test_topic_written_by_superuser (Any): 管理者が作成したテスト用お題
        test_db (Any): テスト用DB接続
        superuser_token_headers (Any): テスト用管理者ユーザーの認証用JWTトークンヘッダー
    """
    response = client.delete(
        f"/api/v1/topics/{test_topic_written_by_superuser.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert test_db.query(models.Topic).filter(not models.Topic.is_visible).all() == []


def test_delete_topic_by_others(
    client, test_topic_written_by_superuser, test_db, user_token_headers
):
    """
    test_delete_topic_by_others 管理者以外の他人がお題を削除するテスト

    Args:
        client (Any): HTTPクライアント
        test_topic_written_by_superuser (Any): 管理者が作成したテスト用お題
        test_db (Any): テスト用DB接続
        user_token_headers (Any): テスト用一般ユーザーの認証用JWTトークンヘッダー
    """
    response = client.delete(
        f"/api/v1/topics/{test_topic_written_by_superuser.id}",
        headers=user_token_headers,
    )
    assert response.status_code == 403
    assert (
        test_db.query(models.Topic)
        .filter(models.Topic.id == test_topic_written_by_superuser.id)
        .first()
        == test_topic_written_by_superuser
    )


def test_delete_my_topic_by_superuser(
    client, test_topic, test_db, superuser_token_headers
):
    """
    test_delete_my_topic_by_superuser 一般ユーザーが作成したお題を管理者が削除するテスト

    Args:
        client (Any): HTTPクライアント
        test_topic (Any): 一般ユーザーが作成したテスト用お題
        test_db (Any): テスト用DB接続
        superuser_token_headers (Any): テスト用管理者ユーザーの認証用JWTトークンヘッダー
    """
    response = client.delete(
        f"/api/v1/topics/{test_topic.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert test_db.query(models.Topic).filter(not models.Topic.is_visible).all() == []


def test_delete_topic_is_not_found(
    client, test_db, superuser_token_headers
):
    """
    test_delete_topic_is_not_found 登録されていないお題を削除できないテスト

    Args:
        client (Any): HTTPクライアント
        test_db (Any): テスト用DB接続
        superuser_token_headers (Any): テスト用管理者ユーザーの認証用JWTトークンヘッダー
    """
    response = client.delete("/api/v1/topics/9999", headers=superuser_token_headers)
    assert response.status_code == 404
    assert (
        test_db.query(models.Topic)
        .filter(models.Topic.id == 9999)
        .first() is None
    )
