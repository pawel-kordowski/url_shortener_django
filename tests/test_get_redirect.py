import pytest
from django.urls import reverse

from tests.url_factory import UrlFactory


@pytest.mark.django_db
def test_get_redirect_returns_404_when_short_not_found(
    client, django_assert_num_queries
):
    url = reverse("get_redirect", kwargs={"short": "notexisting"})

    with django_assert_num_queries(1):
        response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_get_redirect_returns_302_when_short_found(client, django_assert_num_queries):
    url_object = UrlFactory()
    url = reverse("get_redirect", kwargs={"short": url_object.short})

    with django_assert_num_queries(1):
        response = client.get(url)

    assert response.status_code == 302
    assert response.headers["location"] == url_object.url


@pytest.mark.parametrize("method", ("POST", "DELETE", "PUT", "PATCH"))
def test_only_get_method_is_allowed_for_get_redirect(method, client):
    url = reverse("get_redirect", kwargs={"short": "notexisting"})

    response = client.generic(method, url)

    assert response.status_code == 405
