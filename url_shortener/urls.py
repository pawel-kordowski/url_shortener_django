from django.urls import include, path

urlpatterns = [path("", include("url_shortener_app.urls"))]
