import pytest

from tests.factories import AdFactory


@pytest.mark.django_db
def test_ad_create(client, category, user):
    ad = AdFactory.create()

    response = client.post(
        "/ad/create/",
        {
            "name": "test ad name",
            "author": user.id,
            "price": 56,
            "description": "test_description",
            "is_published": False,
            "category": category.id,
        },
        content_type="application/json"
    )

    expected_response = {
        "id": 2,
        "name": "test ad name",
        "price": 56,
        "description": "test_description",
        "is_published": False,
        "image": ad.image.url if ad.image else None,
        "category": category.id,
        "author": user.id,
    }

    assert response.status_code == 201
    assert response.data == expected_response
