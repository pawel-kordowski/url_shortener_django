from unittest.mock import patch, call

import pytest
from django.conf import settings
from django.urls import reverse

from tests.url_factory import UrlFactory
from url_shortener_app.models import Url


@pytest.mark.django_db
@patch("url_shortener_app.serializers.RandomStringGenerator.get_random_string")
class TestCreateUrl:
    url = reverse("urls-list")
    full_url = "http://google.com"

    def test_create_url_successful(self, mocked_get_random_string, django_assert_num_queries, client):
        short = "short"
        mocked_get_random_string.return_value = short

        with django_assert_num_queries(2):
            response = client.post(self.url, data={"url": self.full_url})

        assert response.status_code == 201
        assert response.json() == {
            "orig_url": self.full_url,
            "short_url": f"http://testserver/{short}/"
        }
        all_urls_from_db = Url.objects.all()
        assert len(all_urls_from_db) == 1
        created_url = all_urls_from_db[0]
        assert created_url.url == self.full_url
        assert created_url.short == short
        mocked_get_random_string.assert_called_once_with(length=settings.SHORT_URL_MIN_LENGTH)

    def test_create_url_short_already_taken_5_times(self, mocked_get_random_string, django_assert_num_queries, client):
        taken_short = "short_1"
        UrlFactory(short=taken_short)
        another_short = "short_2"
        mocked_get_random_string.side_effect = [taken_short] * 5 + [another_short]

        with django_assert_num_queries(7):
            response = client.post(self.url, data={"url": self.full_url})

        assert response.status_code == 201
        mocked_get_random_string.assert_has_calls([call(length=settings.SHORT_URL_MIN_LENGTH)] * 5 + [call(length=settings.SHORT_URL_MIN_LENGTH + 1)])
        assert Url.objects.count() == 2

    @pytest.mark.parametrize(
        "http_method", ("GET", "DELETE", "PATCH", "PUT")
    )
    def test_only_post_method_is_allowed(self, mocked_get_random_string, http_method, client):
        response = client.generic(http_method, self.url)

        assert response.status_code == 405
