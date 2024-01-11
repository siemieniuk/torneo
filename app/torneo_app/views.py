import random
from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.db.models import Value
from django.db.models.functions import Concat
from django.http import Http404, HttpRequest, HttpResponseForbidden, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView

from torneo_app.forms import ResultForm, TournamentApplyForm, TournamentModelForm
from torneo_app.models import Result, Tournament, TournamentAssignment
from torneo_app.service import fetch_result_to_fill, get_tournament_and_statuses
from torneo_app.utils import UserStatus, now
from users.models import MyUser


def index(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("my_page")
    return render(request, "index.html")


def custom_page_unauthorized(request: HttpRequest, *args, **argv):
    return render(request, "403.html", status=403)


def custom_page_not_found(request: HttpRequest, *args, **argv):
    return render(request, "404.html", status=404)


def custom_page_unauthorized(request: HttpRequest, *args, **argv):
    return render(request, "500.html", status=500)


def browse_tournaments(request: HttpRequest):
    search = request.GET.get("search", "").strip()
    tournaments = Tournament.objects.filter(
        applying_deadline__gt=now(), name__icontains=search
    ).order_by("applying_deadline")

    paginator = Paginator(tournaments, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request, "tournament/browse_tournaments.html", {"page_obj": page_obj}
    )


@login_required()
def my_page(request: HttpRequest):
    applied_tournaments = Tournament.objects.filter(
        tournamentassignment__player=request.user.id
    )

    organized_tournaments = Tournament.objects.filter(
        organizer=request.user.id
    )

    return render(
        request,
        "tournament/my_page.html",
        {
            "applied_tournaments": applied_tournaments,
            "organized_tournaments": organized_tournaments,
        },
    )


@login_required()
def apply_for_tournament(request: HttpRequest, tournament_id: int):
    try:
        tournament, user_statuses = get_tournament_and_statuses(
            request.user, tournament_id
        )
    except Tournament.DoesNotExist:
        raise Http404

    if UserStatus.APPLIED in user_statuses:
        messages.error(request, "You have already applied to this tournament!")
        return redirect("tournament_detail", tournament_id=tournament_id)

    if (
        tournament.max_number_of_participants
        == tournament.applied_participants_count
    ):
        messages.error(
            request,
            "You cannot apply to this tournament; the number of players is maximal",
        )
        return redirect("tournament_detail", tournament_id=tournament_id)

    if request.method == "POST":
        form = TournamentApplyForm(
            request.POST, applying_user=request.user, tournament=tournament
        )
        if form.is_valid():
            try:
                form.save()
                messages.success(
                    request,
                    "Successfully applied to the tournament!",
                )
                return redirect(
                    "tournament_detail", tournament_id=tournament_id
                )
            except Exception as e:
                messages.error(
                    request,
                    "Error: This ranking or license number was already used!",
                )

    form = TournamentApplyForm()
    template_params = {"tournament": tournament}
    template_params["form"] = form

    return render(
        request, "tournament/apply_for_tournament.html", template_params
    )


@login_required()
def create_tournament(request: HttpRequest):
    if request.method == "POST":
        form = TournamentModelForm(request.POST, organizer=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Tournament was successfully created!")
            return redirect("my_page")
    else:
        form = TournamentModelForm()
    return render(request, "tournament/create_tournament.html", {"form": form})


@login_required()
def delete_tournament(request: HttpRequest, tournament_id: int):
    tournament, statuses = get_tournament_and_statuses(
        request.user.id, tournament_id
    )
    if UserStatus.ORGANIZER not in statuses:
        raise HttpResponseForbidden()
    if request.method == "POST":
        tournament.delete()
        messages.success(request, "Tournament was successfully deleted!")
        return redirect("my_page")
    else:
        return render(
            request,
            "tournament/delete_tournament.html",
            {"tournament": tournament},
        )


@login_required()
def update_tournament(request: HttpRequest, tournament_id: int):
    try:
        tournament, statuses = get_tournament_and_statuses(
            request.user.id, tournament_id, with_sponsors=True
        )
    except Tournament.DoesNotExist:
        raise Http404

    if UserStatus.ORGANIZER not in statuses:
        raise HttpResponseForbidden()

    if request.method == "POST":
        form = TournamentModelForm(
            request.POST, organizer=request.user, instance=tournament, update=True
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated")
            return redirect("tournament_detail", tournament_id=tournament.id)
    else:
        form = TournamentModelForm(instance=tournament, update=True)
    return render(
        request,
        "tournament/edit_tournament.html",
        {"form": form, "tournament": tournament},
    )


class TournamentView(TemplateView):
    template_name = "tournament/tournament_detail.html"

    user = None
    tournament = None
    statuses = None
    tournament_was_deleted = False

    def setup(self, request, *args, **kwargs):
        try:
            self.tournament, self.statuses = get_tournament_and_statuses(
                request.user.id, kwargs.get("tournament_id")
            )
            self.user = request.user
            if (
                self.tournament.has_started
                and self.tournament.is_ladder_created == False
            ):
                self._try_to_create_ladder()
        except Tournament.DoesNotExist:
            self.tournament = None

        super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if self.tournament_was_deleted:
            messages.error(
                request,
                "Due to insufficient number of players, "
                "this tournament was deleted.",
            )
            return redirect("index")
        if self.tournament is None:
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["tournament"] = self.tournament
        if UserStatus.APPLIED in self.statuses:
            context["has_applied"] = True
        if UserStatus.ORGANIZER in self.statuses:
            context["is_organizer"] = True
        context["result"] = fetch_result_to_fill(
            self.user.id, self.tournament.pk
        )
        return context

    def _try_to_create_ladder(self):
        players = list(
            TournamentAssignment.objects.filter(tournament=self.tournament)
            .values("player")
            .all()
        )

        players = [p["player"] for p in players]

        if self._is_len_power_of_two(players) == False:
            self.tournament.delete()
            self.tournament_was_deleted = True
            return

        players = list(MyUser.objects.filter(pk__in=players))

        random.shuffle(players)
        mid = len(players) // 2
        objects_to_save = []
        for player1, player2, match_id in zip(
            players[:mid], players[mid:], range(mid, len(players))
        ):
            res = Result(
                player_1=player1,
                player_2=player2,
                match_id=match_id,
                tournament=self.tournament,
            )
            objects_to_save.append(res)

        for i in range(mid):
            res = Result(match_id=i, tournament=self.tournament)
            objects_to_save.append(res)

        try:
            with transaction.atomic():
                for object in objects_to_save:
                    object.save()
                self.tournament.is_ladder_created = True
                self.tournament.save(updated=True)
        except IntegrityError:
            pass

    @staticmethod
    def _is_len_power_of_two(players):
        N = len(players)
        i = 2
        while i < N:
            i **= 2
        return i == N


@method_decorator(login_required, name="dispatch")
class ResultView(UpdateView):
    model = Result
    template_name = "tournament/add_result.html"
    form_class = ResultForm

    def form_valid(self, form) -> HttpResponse:
        result = form.save()

        nulls = 0
        if result.selected_winner_1 is None:
            nulls += 1
        if result.selected_winner_2 is None:
            nulls += 1

        match nulls:
            case 0:
                self._update_ladder(result)
                messages.success(
                    self.request,
                    "After your submission, "
                    "the tournament ladder was updated",
                )
            case 1:
                messages.success(
                    self.request, "Your result was correctly saved"
                )
            case 2:
                messages.error(self.request, "Conflicting winners: ")
                return redirect(
                    "tournament_detail", tournament_id=result.tournament.pk
                )
            case _:
                pass
        return super(ResultView, self).form_valid(form)

    def dispatch(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        user_id = request.user.id
        result = self.get_object()
        if user_id != result.player_1.pk and user_id != result.player_2.pk:
            messages.error(
                request,
                "You are not allowed to watch the requested site",
            )
            return redirect("index")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["result"] = self.get_object()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user.id
        return kwargs

    def get_success_url(self) -> str:
        return reverse_lazy(
            "tournament_detail",
            kwargs={"tournament_id": self.get_object().tournament.pk},
        )

    def _update_ladder(self, result):
        result_to_update = Result.objects.get(
            tournament=result.tournament, match_id=result.match_id // 2
        )
        winning_player = MyUser.objects.get(pk=result.selected_winner_1)
        if result.match_id % 2 == 1:
            result_to_update.player_1 = winning_player
        else:
            result_to_update.player_2 = winning_player
        result_to_update.save()


def fetch_results(request: HttpRequest, tournament_id: int):
    tournament = Tournament.objects.get(id=tournament_id)

    if request.method == "GET":
        results = list(
            Result.objects.annotate(
                p1=Concat(
                    "player_1__first_name", Value(" "), "player_1__last_name"
                ),
                p2=Concat(
                    "player_2__first_name", Value(" "), "player_2__last_name"
                ),
            )
            .filter(tournament=tournament)
            .values(
                "p1",
                "p2",
                "player_1__pk",
                "player_2__pk",
                "match_id",
            )
            .order_by("-match_id")
        )

        n = results[0]["match_id"]
        gen_seed = n
        remaining = (n + 1) // 2

        data = []
        while True:
            row = []
            for _ in range(remaining):
                result = results.pop(0)
                p1 = dict()
                p1["name"] = result["p1"]
                p1["seed"] = result["player_1__pk"]
                p1["id"] = result["player_1__pk"]
                p2 = dict()
                p2["name"] = result["p2"]
                p2["seed"] = result["player_2__pk"]
                p2["id"] = result["player_2__pk"]
                row.append([p1, p2])
            data.append(row)
            if remaining > 0:
                remaining //= 2
            else:
                break

        return JsonResponse(
            data,
            content_type="application/json",
            safe=False,
            json_dumps_params={"ensure_ascii": False},
        )
    else:
        return JsonResponse(
            data={"message": "Invalid method"},
            content_type="application/json",
            status=405,
        )
