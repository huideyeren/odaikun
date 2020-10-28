from app.db.models import topic_table


def test_get_topics(client, test_topic, user_token_headers):
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
    response = client.delete(
        f"/api/v1/topics/{test_topic.id}", headers=user_token_headers
    )
    assert response.status_code == 200
    assert test_db.query(topic_table.Topic).filter(not topic_table.Topic.is_visible).all() == []


def test_delete_topic_on_superuser(
    client, test_topic_written_by_superuser, test_db, superuser_token_headers
):
    response = client.delete(
        f"/api/v1/topics/{test_topic_written_by_superuser.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert test_db.query(topic_table.Topic).filter(not topic_table.Topic.is_visible).all() == []


def test_delete_topic_by_others(
    client, test_topic_written_by_superuser, test_db, user_token_headers
):
    response = client.delete(
        f"/api/v1/topics/{test_topic_written_by_superuser.id}",
        headers=user_token_headers,
    )
    assert response.status_code == 403
    assert (
        test_db.query(topic_table.Topic)
        .filter(topic_table.Topic.id == test_topic_written_by_superuser.id)
        .first()
        == test_topic_written_by_superuser
    )


def test_delete_my_topic_by_superuser(
    client, test_topic, test_db, superuser_token_headers
):
    response = client.delete(
        f"/api/v1/topics/{test_topic.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert test_db.query(topic_table.Topic).filter(not topic_table.Topic.is_visible).all() == []


def test_delete_topic_is_not_found(
    client, test_topic_written_by_superuser, test_db, superuser_token_headers
):
    response = client.delete("/api/v1/topics/9999", headers=superuser_token_headers)
    assert response.status_code == 404
    assert (
        test_db.query(topic_table.Topic)
        .filter(topic_table.Topic.id == test_topic_written_by_superuser.id)
        .first()
        == test_topic_written_by_superuser
    )
