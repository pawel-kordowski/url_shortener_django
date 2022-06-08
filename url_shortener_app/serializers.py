from django.conf import settings
from django.urls import reverse
from rest_framework import serializers

from url_shortener_app.models import Url
from url_shortener_app.random_string_generator import RandomStringGenerator


class UrlSerializer(serializers.ModelSerializer):
    url = serializers.CharField(write_only=True)
    orig_url = serializers.CharField(source="url", read_only=True)
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = Url
        fields = ["url", "orig_url", "short_url"]

    def get_short_url(self, url: Url) -> str:
        location = reverse("get_redirect", kwargs={"short": url.short})
        absolute_uri = self.context["request"].build_absolute_uri(location=location)
        return absolute_uri

    @staticmethod
    def _get_not_used_short() -> str:
        short_length = settings.SHORT_URL_MIN_LENGTH
        tries_count = 0
        while True:
            short = RandomStringGenerator.get_random_string(length=short_length)
            if not Url.objects.filter(short=short).exists():
                return short
            tries_count += 1
            if tries_count == 5:
                short_length += 1
                tries_count = 0

    def save(self, **kwargs):
        kwargs["short"] = self._get_not_used_short()
        return super().save(**kwargs)
