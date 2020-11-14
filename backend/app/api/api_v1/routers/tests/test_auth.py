from app.core import security

# Monkey patch function we can use to shave a second off our tests
# by skipping the password hashing check


def verify_password_mock(first: str, second: str):
    """
    verify_password_mock パスワードのモック

    Args:
        first (str): 第一の文字列
        second (str): 第二の文字列

    Returns:
        True: 常にTrueを返す
    """
    return True


def test_login(client, test_user, monkeypatch):
    """
    test_login ログインのテスト。
    ステータスコードが200（OK）なら問題なし。

    Args:
        client (Any): HTTPクライアント
        test_user (Any): テスト用のユーザー
        monkeypatch (Any): パスワードのハッシュ化をスキップし、常に通す。
    """
    # Patch the test to skip password hashing check for speed
    monkeypatch.setattr(security, "verify_password", verify_password_mock)

    response = client.post(
        "/api/token",
        data={"username": test_user.email, "password": "nottheactualpass"},
    )
    assert response.status_code == 200


def test_signup(client, monkeypatch):
    """
    test_signup サインアップのテスト。
    ステータスコードが200（OK）なら問題なし。

    Args:
        client (Any): HTTPクライアント
        monkeypatch (Any): パスワードのハッシュ化をスキップし、常に通す。
    """

    def get_password_hash_mock(first: str, second: str):
        return True

    monkeypatch.setattr(security, "get_password_hash", get_password_hash_mock)

    response = client.post(
        "/api/signup",
        data={"username": "some@email.com", "password": "randompassword"},
    )
    assert response.status_code == 200


def test_resignup(client, test_user, monkeypatch):
    """
    test_resignup 再サインアップのテスト。
    ステータスコードが409（要調査）なら問題なし。

    Args:
        client (Any): HTTPクライアント
        test_user (Any): テスト用のユーザー
        monkeypatch (Any): パスワードのハッシュ化をスキップし、常に通す。
    """
    # Patch the test to skip password hashing check for speed
    monkeypatch.setattr(security, "verify_password", verify_password_mock)

    response = client.post(
        "/api/signup",
        data={
            "username": test_user.email,
            "password": "password_hashing_is_skipped_via_monkey_patch",
        },
    )
    assert response.status_code == 409


def test_wrong_password(client, test_db, test_user, test_password, monkeypatch):
    """
    test_wrong_password 違うパスワードが投げられたときのテスト。
    ステータスコードが401（認証エラー）なら問題なし。

    Args:
        client (Any): HTTPクライアント
        test_db (Any): テスト用のDB接続
        test_user (Any): テスト用のユーザー
        test_password (Any): テスト用のパスワード
        monkeypatch (Any): パスワードのハッシュ化をスキップし、常に通さない。
    """

    def verify_password_failed_mock(first: str, second: str):
        """
        verify_password_failed_mock パスワードを通さないようにするためのモック

        Args:
            first (str): 第一の文字列
            second (str): 第二の文字列

        Returns:
            False: 常にFalseを返す
        """
        return False

    monkeypatch.setattr(security, "verify_password", verify_password_failed_mock)

    response = client.post(
        "/api/token", data={"username": test_user.email, "password": "wrong"}
    )
    assert response.status_code == 401


def test_wrong_login(client, test_db, test_user, test_password):
    """
    test_wrong_login 間違った情報でログインしたときのテスト。
    ステータスコードが401（認証エラー）なら問題なし。

    Args:
        client ([type]): [description]
        test_db ([type]): [description]
        test_user ([type]): [description]
        test_password ([type]): [description]
    """
    response = client.post(
        "/api/token", data={"username": "fakeuser", "password": test_password}
    )
    assert response.status_code == 401
