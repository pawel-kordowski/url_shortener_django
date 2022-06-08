import pytest
from django.core.cache import cache
from django.urls import reverse

from tests.factories.url_factory import UrlFactory


@pytest.mark.django_db
def test_get_redirect_returns_404_when_short_not_found(
    client, django_assert_num_queries
):
    url = reverse("get_redirect", kwargs={"short": "notexisting"})

    with django_assert_num_queries(1):
        response = client.get(url)

    assert response.status_code == 404

    # use cache
    with django_assert_num_queries(0):
        response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_get_redirect_returns_302_when_short_found(client, django_assert_num_queries):
    url_object = UrlFactory()
    url = reverse("get_redirect", kwargs={"short": url_object.short})

    # use cache
    with django_assert_num_queries(0):
        response = client.get(url)

    assert response.status_code == 302
    assert response.headers["location"] == url_object.url

    # with no cache
    cache.clear()

    with django_assert_num_queries(1):
        response = client.get(url)

    assert response.status_code == 302
    assert response.headers["location"] == url_object.url


@pytest.mark.parametrize("http_method", ("POST", "DELETE", "PUT", "PATCH"))
def test_only_get_method_is_allowed_for_get_redirect(http_method, client):
    url = reverse("get_redirect", kwargs={"short": "notexisting"})

    response = client.generic(http_method, url)

    assert response.status_code == 405
