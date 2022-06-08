from django.urls import include, path
from rest_framework.routers import DefaultRouter

from url_shortener_app import views, viewsets

router = DefaultRouter()
router.register(r"urls", viewsets.UrlCreateViewSet, basename="urls")

urlpatterns = [
    path("", include(router.urls)),
    path("<str:short>/", views.get_redirect, name="get_redirect"),
]
