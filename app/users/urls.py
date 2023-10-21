from django.contrib.auth import views as auth_views
from django.urls import include, path

from users.views import register_view

urlpatterns = [
    path("register/", register_view, name="register"),
    path("", include("django.contrib.auth.urls")),
]
