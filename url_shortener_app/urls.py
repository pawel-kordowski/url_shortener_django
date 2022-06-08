from django.urls import path

from url_shortener_app import views

urlpatterns = [path("<str:short>/", views.get_redirect, name="get_redirect")]
