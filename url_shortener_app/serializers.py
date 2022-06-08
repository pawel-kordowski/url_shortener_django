from django.urls import reverse
from rest_framework import serializers

from url_shortener_app.models import Url


class UrlSerializer(serializers.ModelSerializer):
    url = serializers.URLField(write_only=True)
    orig_url = serializers.URLField(source="url", read_only=True)
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = Url
        fields = ["url", "orig_url", "short_url"]

    def get_short_url(self, url: Url) -> str:
        location = reverse("get_redirect", kwargs={"short": url.short})
        absolute_uri = self.context["request"].build_absolute_uri(location=location)
        return absolute_uri
