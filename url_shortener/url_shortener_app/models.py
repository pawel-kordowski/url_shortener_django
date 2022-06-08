from django.db import models


class Url(models.Model):
    short = models.CharField(max_length=10, unique=True, db_index=True)
    url = models.URLField(max_length=2048)
