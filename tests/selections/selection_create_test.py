import pytest


@pytest.mark.django_db
def test_selection_create(client, user_token, user, ad):
    response = client.post(
        "/selection/create/",
        {
            "name": "test selection name",
            "owner": user.id,
            "items": [ad.id]
        },
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {user_token}"
    )

    expected_response = {
        "id": 1,
        "name": "test selection name",
        "owner": user.id,
        "items": [ad.id]
    }

    assert response.status_code == 201
    assert response.data == expected_response
