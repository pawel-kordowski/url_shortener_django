from unittest.mock import call, patch

import pytest
from django.conf import settings

from tests.factories.url_factory import UrlFactory
from url_shortener_app.models import Url

pytestmark = pytest.mark.django_db


def test_url_get_orig_url_by_short_returns_url_when_found():
    url = UrlFactory()

    orig_url = Url.objects.get_orig_url_by_short(short=url.short)

    assert orig_url == url.url


def test_url_get_orig_url_by_short_raises_exception_when_not_found():
    with pytest.raises(Url.DoesNotExist):
        Url.objects.get_orig_url_by_short(short="not_existing")


@patch("url_shortener_app.models.RandomStringGenerator.get_random_strings")
def test_get_not_used_short_returns_new_short(mocked_get_random_strings):
    urls = UrlFactory.create_batch(size=settings.SHORT_URL_CANDIDATES_COUNT)
    new_short = "new_short"
    mocked_get_random_strings.side_effect = [{url.short for url in urls}, {new_short}]

    short = Url.objects.get_not_used_short()

    assert short == new_short
    mocked_get_random_strings.assert_has_calls(
        [
            call(
                length=settings.SHORT_URL_MIN_LENGTH,
                count=settings.SHORT_URL_CANDIDATES_COUNT,
            ),
            call(
                length=settings.SHORT_URL_MIN_LENGTH + 1,
                count=settings.SHORT_URL_CANDIDATES_COUNT,
            ),
        ]
    )


@patch("url_shortener_app.models.UrlQuerySet.get_not_used_short")
def test_save_url_computes_short(mocked_get_not_used_short):
    short = "short"
    mocked_get_not_used_short.return_value = short
    url = Url(url="http://google.com")
    url.save()
    url.refresh_from_db()

    assert url.short == short
    mocked_get_not_used_short.assert_called_once_with()
