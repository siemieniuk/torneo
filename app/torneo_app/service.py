from typing import List

from django.db.models import Q

from torneo_app.models import Result, Tournament, TournamentAssignment
from torneo_app.utils import UserStatus


def fetch_result_to_fill(user_id: int | None, tournament_id: int) -> bool:
    if user_id is None:
        return False
    result = Result.objects.filter(
        Q(tournament=tournament_id)
        & (~Q(player_1=None))
        & (~Q(player_2=None))
        & (
            (Q(player_1=user_id) & Q(selected_winner_1=None))
            | (Q(player_2=user_id) & Q(selected_winner_2=None))
        )
    ).first()
    return result


def get_tournament_and_statuses(
    user_id: int, tournament_id: int, with_sponsors: bool = False
) -> tuple[Tournament, List[UserStatus]]:
    tournament = Tournament.objects.get(id=tournament_id)
    if with_sponsors:
        tournament.sponsors.all()

    statuses = []
    if tournament.organizer.id == user_id:
        statuses.append(UserStatus.ORGANIZER)

    tournament_assignment = TournamentAssignment.objects.filter(
        tournament=tournament_id, player=user_id
    )

    if tournament_assignment.exists():
        statuses.append(UserStatus.APPLIED)

    if UserStatus == []:
        statuses.append(UserStatus.NORMAL)

    return tournament, statuses
