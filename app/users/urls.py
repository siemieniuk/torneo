from django.contrib.auth import views as auth_views
from django.urls import include, path

from users.views import activate, register_view

urlpatterns = [
    path("register/", register_view, name="register"),
    path("", include("django.contrib.auth.urls")),
    path(
        "activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/",
        activate,
        name="activate",
    ),
]
