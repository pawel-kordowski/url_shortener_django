from rest_framework import viewsets, mixins

from url_shortener_app.serializers import UrlSerializer


class UrlCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UrlSerializer
