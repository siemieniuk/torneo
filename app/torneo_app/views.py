import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import ListView

from torneo_app.models import MyUser, Tournament, TournamentAssignment
from torneo_app.utils import UserStatus, now, str_empty


def get_tournament_and_status(
    user_id: int, tournament_id: int
) -> tuple[Tournament, UserStatus]:
    tournament = Tournament.objects.get(id=tournament_id)

    if tournament.organizer.id == user_id:
        return tournament, UserStatus.ORGANIZER

    tournament_assignment = TournamentAssignment.objects.filter(
        tournament=tournament_id, player=user_id
    ).all()

    if len(tournament_assignment) > 0:
        return tournament, UserStatus.APPLIED
    return tournament, UserStatus.NORMAL


def index(request: HttpRequest):
def custom_page_unauthorized(request: HttpRequest, *args, **argv):
    return render(request, "403.html", status=403)


def custom_page_not_found(request: HttpRequest, *args, **argv):
    return render(request, "404.html", status=404)


def custom_page_unauthorized(request: HttpRequest, *args, **argv):
    return render(request, "500.html", status=500)


    search = request.GET.get("search", "").strip()
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
    my_tournaments = Tournament.objects.filter(
        tournamentassignment__player=request.user.id
    )

    return render(request, "tournament/my_page.html", {"tournaments": my_tournaments})


# TODO: Write form
# TODO: Template - render cases when organizer or user
@login_required()
def apply_for_tournament(request: HttpRequest, tournament_id: int):
    if request.method == "GET":
        try:
            tournament, user_status = get_tournament_and_status(
                request.user, tournament_id
            )
            template_params = {"tournament": tournament}
        except Tournament.DoesNotExist:
            return HttpResponseNotFound("Tournament not found")

        match (user_status):
            case UserStatus.APPLIED:
                template_params["has_applied"] = True
            case UserStatus.ORGANIZER:
                template_params["is_organizer"] = True
            case _:
                pass

        return render(request, "tournament/apply_for_tournament.html", template_params)
    else:
        pass


# TODO: Template - render cases when organizer or user
def read_tournament(request: HttpRequest, tournament_id: int):
    try:
        tournament, user_status = get_tournament_and_status(
            request.user.id, tournament_id
        )
    except Tournament.DoesNotExist:
        return HttpResponseNotFound("Tournament not found")

    template_params = {"tournament": tournament}

    match (user_status):
        case UserStatus.APPLIED:
            template_params["has_applied"] = True
        case UserStatus.ORGANIZER:
            template_params["is_organizer"] = True

    return render(request, "tournament/tournament_detail.html", template_params)
