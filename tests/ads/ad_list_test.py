import pytest

from tests.factories import AdFactory


@pytest.mark.django_db
def test_ads_list(client):
    ads_factory = AdFactory.create_batch(5)

    response = client.get('/ad/')

    ads = []
    for ad in ads_factory:
        ads.append(
            {
                "id": ad.id,
                "name": ad.name,
                "author_id": ad.author_id,
                "author": ad.author.first_name,
                "price": ad.price,
                "description": ad.description,
                "is_published": ad.is_published,
                "category_id": ad.category_id,
                "image": ad.image.url if ad.image else None,
            }
        )

    expected_response = {
        'items': ads,
        'num_pages': 1,
        'total': 5,
    }

    assert response.status_code == 200
    assert response.json() == expected_response
