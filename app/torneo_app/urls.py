from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tournament/create", views.create_tournament, name="new_tournament"),
    path(
        "tournament/<int:tournament_id>",
        views.read_tournament,
        name="tournament_detail",
    ),
    path(
        "tournament/<int:tournament_id>/apply",
        views.apply_for_tournament,
        name="tournament_apply",
    ),
    path("me", views.my_page, name="my_page"),
]
