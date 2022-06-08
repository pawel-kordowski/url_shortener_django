from __future__ import annotations

from django.conf import settings
from django.db import models

from url_shortener_app.random_string_generator import RandomStringGenerator


class UrlQuerySet(models.QuerySet):
    def get_by_short(self, short: str) -> Url:
        return self.get(short=short)

    def get_not_used_short(self) -> str:
        short_length = settings.SHORT_URL_MIN_LENGTH
        tries_count = 0
        while True:
            short = RandomStringGenerator.get_random_string(length=short_length)
            if not self.filter(short=short).exists():
                return short
            tries_count += 1
            if tries_count == 5:
                short_length += 1
                tries_count = 0


class Url(models.Model):
    objects = UrlQuerySet.as_manager()

    short = models.CharField(max_length=10, unique=True, db_index=True)
    url = models.URLField(max_length=2048)

    def save(self, *args, **kwargs):
        if not self.short:
            self.short = Url.objects.get_not_used_short()
        return super().save(*args, **kwargs)
