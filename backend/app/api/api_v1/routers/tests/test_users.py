from app.db import models


def test_get_users(client, test_superuser, superuser_token_headers):
    """
    test_get_users ユーザー情報を取得するテスト

    Args:
        client (Any): HTTPクライアント
        test_superuser (Any): テスト用管理者
        superuser_token_headers (Any): テスト用管理者ユーザーの認証用JWTトークンヘッダー
    """
    response = client.get("/api/v1/users", headers=superuser_token_headers)
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": test_superuser.id,
            "email": test_superuser.email,
            "is_active": test_superuser.is_active,
            "is_superuser": test_superuser.is_superuser,
        }
    ]


def test_delete_user(client, test_superuser, test_db, superuser_token_headers):
    """
    test_delete_user ユーザーを削除するテスト

    Args:
        client (Any): HTTPクライアント
        test_superuser (Any): テスト用管理者
        test_db (Any): テスト用DB接続
        superuser_token_headers (Any): テスト用管理者ユーザーの認証用JWTトークンヘッダー
    """
    response = client.delete(
        f"/api/v1/users/{test_superuser.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert test_db.query(models.User).all() == []


def test_delete_user_not_found(client, superuser_token_headers):
    """
    test_delete_user_not_found 削除するユーザーが見当たらない場合のテスト

    Args:
        client (Any): HTTPクライアント
        superuser_token_headers (Any): テスト用管理者ユーザーの認証用JWTトークンヘッダー
    """
    response = client.delete("/api/v1/users/4321", headers=superuser_token_headers)
    assert response.status_code == 404


def test_edit_user(client, test_superuser, superuser_token_headers):
    """
    test_edit_user ユーザーを編集するテスト

    Args:
        client (Any): HTTPクライアント
        test_superuser (Any): テスト用管理者
        superuser_token_headers (Any): テスト用管理者ユーザーの認証用JWTトークンヘッダー
    """
    new_user = {
        "email": "newemail@email.com",
        "is_active": False,
        "is_superuser": True,
        "first_name": "Joe",
        "last_name": "Smith",
        "password": "new_password",
    }

    response = client.put(
        f"/api/v1/users/{test_superuser.id}",
        json=new_user,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    new_user["id"] = test_superuser.id
    new_user.pop("password")
    assert response.json() == new_user


def test_edit_user_not_found(client, superuser_token_headers):
    """
    test_edit_user_not_found 編集するユーザーが見当たらない場合のテスト

    Args:
        client (Any): HTTPクライアント
        superuser_token_headers (Any): テスト用管理者ユーザーの認証用JWTトークンヘッダー
    """
    new_user = {
        "email": "newemail@email.com",
        "is_active": False,
        "is_superuser": False,
        "password": "new_password",
    }
    response = client.put(
        "/api/v1/users/1234", json=new_user, headers=superuser_token_headers
    )
    assert response.status_code == 404


def test_get_user(
    client,
    test_user,
    superuser_token_headers,
):
    """
    test_get_user 指定したIDのユーザー情報を取得するテスト

    Args:
        client (Any): HTTPクライアント
        test_user (Any): テスト用ユーザーデータ
        superuser_token_headers (Any): テスト用管理者ユーザーの認証用JWTトークンヘッダー
    """
    response = client.get(
        f"/api/v1/users/{test_user.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": test_user.id,
        "email": test_user.email,
        "is_active": bool(test_user.is_active),
        "is_superuser": test_user.is_superuser,
    }


def test_user_not_found(client, superuser_token_headers):
    """
    test_user_not_found 実在しないユーザー情報を取得するテスト

    Args:
        client (Any): HTTPクライアント
        superuser_token_headers (Any): テスト用管理者ユーザーの認証用JWTトークンヘッダー
    """
    response = client.get("/api/v1/users/123", headers=superuser_token_headers)
    assert response.status_code == 404


def test_authenticated_user_me(client, user_token_headers):
    """
    test_authenticated_user_me 認証済みのユーザー情報が取得できるかのテスト

    Args:
        client (Any): HTTPクライアント
        user_token_headers (Any): テスト用一般ユーザーの認証用JWTトークンヘッダー
    """
    response = client.get("/api/v1/users/me", headers=user_token_headers)
    assert response.status_code == 200


def test_unauthenticated_routes(client):
    """
    test_unauthenticated_routes 未認証の状態で情報が取得できないことのテスト

    Args:
        client (Any): HTTPクライアント
    """
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401
    response = client.get("/api/v1/users")
    assert response.status_code == 401
    response = client.get("/api/v1/users/123")
    assert response.status_code == 401
    response = client.put("/api/v1/users/123")
    assert response.status_code == 401
    response = client.delete("/api/v1/users/123")
    assert response.status_code == 401


def test_unauthorized_routes(client, user_token_headers):
    """
    test_unauthorized_routes 権限の無いURLにアクセスできないことのテスト

    Args:
        client (Any): HTTPクライアント
        user_token_headers (Any): テスト用一般ユーザーの認証用JWTトークンヘッダー
    """
    response = client.get("/api/v1/users", headers=user_token_headers)
    assert response.status_code == 403
    response = client.get("/api/v1/users/123", headers=user_token_headers)
    assert response.status_code == 403
