import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import ListView

from torneo_app.models import Tournament, TournamentAssignment
from torneo_app.utils import now, str_empty


def index(request: HttpRequest):
    search = request.GET.get("search", "").strip()
    print(search)
    tournaments = (
        Tournament.objects.filter(applying_deadline__gt=now(), name__icontains=search)
        .select_related()
        .all()
        .order_by("applying_deadline")
    )

    paginator = Paginator(tournaments, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "home.html", {"page_obj": page_obj})


@login_required()
def create_tournament(request: HttpRequest):
    if request.method == "POST":
        pass
    else:
        return render(request, "tournament/create_tournament.html")


@login_required()
def my_page(request: HttpRequest):
    my_tournaments = TournamentAssignment.objects.filter(
        player=request.user
    ).select_related()

    return render(request, "tournament/my_page.html", {"tournaments": my_tournaments})


# TODO: Write form
@login_required()
def apply_for_tournament(request: HttpRequest, id: int):
    if request.method == "GET":
        tournament = Tournament.objects.get(id=id)
        tournament_id = id
        print(tournament.name)
        print(tournament.id)
        if request.user.is_authenticated:
            user_id = request.user.id
            tournament_assignment = TournamentAssignment.objects.filter(
                tournament=tournament_id, player=user_id
            )
        return render(
            request, "tournament/apply_for_tournament.html", {"tournament": tournament}
        )
    else:
        pass


def read_tournament(request: HttpRequest, id: int):
    try:
        tournament = Tournament.objects.get(id=id)
        return render(
            request, "tournament/tournament_detail.html", {"tournament": tournament}
        )
    except Tournament.DoesNotExist:
        return HttpResponseNotFound("Tournament not found")
