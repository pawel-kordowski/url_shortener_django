from unittest.mock import call, patch

import pytest
from django.conf import settings

from tests.factories.url_factory import UrlFactory
from url_shortener_app.models import Url

pytestmark = pytest.mark.django_db


def test_get_by_short_returns_object_when_found():
    url = UrlFactory()

    url_from_db = Url.objects.get_by_short(short=url.short)

    assert url_from_db == url


def test_get_by_short_raises_exception_when_not_found():
    with pytest.raises(Url.DoesNotExist):
        Url.objects.get_by_short(short="not_existing")


@patch("url_shortener_app.models.RandomStringGenerator.get_random_string")
def test_get_not_used_short_returns_new_short(mocked_get_random_string):
    urls = UrlFactory.create_batch(size=5)
    new_short = "new_short"
    mocked_get_random_string.side_effect = [url.short for url in urls] + [new_short]

    short = Url.objects.get_not_used_short()

    assert short == new_short
    mocked_get_random_string.assert_has_calls(
        [call(length=settings.SHORT_URL_MIN_LENGTH)] * 5
        + [call(length=settings.SHORT_URL_MIN_LENGTH + 1)]
    )
