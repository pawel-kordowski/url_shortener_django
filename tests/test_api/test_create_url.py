import pytest
from django.urls import reverse

from url_shortener_app.models import Url

url = reverse("urls-list")


@pytest.mark.django_db
def test_create_url_successful(django_assert_num_queries, client):
    full_url = "http://google.com"

    with django_assert_num_queries(2):
        response = client.post(url, data={"url": full_url})

    assert response.status_code == 201
    all_urls_from_db = Url.objects.all()
    assert len(all_urls_from_db) == 1
    created_url = all_urls_from_db[0]
    assert created_url.url == full_url
    assert response.json() == {
        "orig_url": full_url,
        "short_url": f"http://testserver/{created_url.short}/",
    }


def test_create_url_requires_url(client):
    response = client.post(url)

    assert response.status_code == 400
    assert response.json() == {"url": ["This field is required."]}


def test_create_url_validates_url(client):
    response = client.post(url, data={"url": "not-valid-url"})

    assert response.status_code == 400
    assert response.json() == {"url": ["Enter a valid URL."]}


@pytest.mark.parametrize("http_method", ("GET", "DELETE", "PATCH", "PUT"))
def test_only_post_method_is_allowed(http_method, client):
    response = client.generic(http_method, url)

    assert response.status_code == 405
