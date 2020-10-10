from app.db import models


def test_get_topics(client, test_topic, user_token_headers):
    response = client.get("/api/v1/topics", headers=user_token_headers)
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": test_topic.id,
            "topic": test_topic.topic,
            "picture_url": test_topic.picture_url,
            "post_date": test_topic.post_date,
            "is_visible": test_topic.is_visible,
            "is_adopted": test_topic.is_adopted,
            "contributor": test_topic.contributor
        }
    ]