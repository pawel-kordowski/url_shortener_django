from __future__ import annotations

from django.conf import settings
from django.db import models

from url_shortener_app.random_string_generator import RandomStringGenerator


class UrlQuerySet(models.QuerySet):
    def get_orig_url_by_short(self, short: str) -> str:
        return self.values("url").get(short=short)["url"]

    def get_not_used_short(self) -> str:
        short_length = settings.SHORT_URL_MIN_LENGTH
        while True:
            short_candidates = RandomStringGenerator.get_random_strings(
                length=short_length, count=settings.SHORT_URL_CANDIDATES_COUNT
            )
            taken_shorts = self.in_bulk(short_candidates, field_name="short").keys()
            not_taken_shorts = short_candidates.difference(taken_shorts)
            if not_taken_shorts:
                return not_taken_shorts.pop()
            short_length += 1


class Url(models.Model):
    objects = UrlQuerySet.as_manager()

    short = models.CharField(max_length=10, unique=True, db_index=True)
    url = models.URLField(max_length=2048)

    def save(self, *args, **kwargs):
        if not self.short:
            self.short = Url.objects.get_not_used_short()
        return super().save(*args, **kwargs)
