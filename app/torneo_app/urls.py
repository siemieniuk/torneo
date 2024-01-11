from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "browse-tournaments",
        views.browse_tournaments,
        name="browse_tournaments",
    ),
    path("tournament/create", views.create_tournament, name="new_tournament"),
    path(
        "tournament/<int:tournament_id>",
        views.TournamentView.as_view(),
        name="tournament_detail",
    ),
    path(
        "tournament/<int:tournament_id>/apply",
        views.apply_for_tournament,
        name="tournament_apply",
    ),
    path(
        "tournament/<int:tournament_id>/update",
        views.update_tournament,
        name="update_tournament",
    ),
    path(
        "tournament/<int:tournament_id>/delete",
        views.delete_tournament,
        name="delete_tournament",
    ),
    path(
        "result/<int:pk>/create",
        views.ResultView.as_view(),
        name="new_result",
    ),
    path(
        "tournament/<int:tournament_id>/results",
        views.fetch_results,
        name="tournament_results",
    ),
    path("me", views.my_page, name="my_page"),
]
