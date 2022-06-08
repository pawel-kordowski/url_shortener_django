from factory import Sequence
from factory.django import DjangoModelFactory

from url_shortener_app.models import Url


class UrlFactory(DjangoModelFactory):
    class Meta:
        model = Url

    short = Sequence(lambda n: f"short{n}")
    url = "http://google.com"
