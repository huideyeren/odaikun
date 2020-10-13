from fastapi import Depends
from fastapi.param_functions import Header
from starlette import responses
from conftest import superuser_token_headers
from app.core.auth import get_current_user
from app.db import models


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
            "id": test_topic.id
        }
    ]

def test_delete_topic_on_superuser(
    client, test_topic, test_db, user_token_headers
):
    response = client.delete(
        f"/api/v1/topics/{test_topic.id}", headers=user_token_headers
    )
    print(f"contributor_id is {test_topic.contributor_id}")
    # print(f"current_user.id is {Depends(get_current_user()).id}")
    assert response.status_code == 200
    assert test_db.query(models.Topic).all() == []
