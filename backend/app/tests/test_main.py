def test_read_main(client):
    """
    test_read_main APIのルートアドレスにアクセスできるかのテスト

    Args:
        client (Any): HTTPクライアント
    """
    response = client.get("/api/v1")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
