import datetime

from fastapi import HTTPException, status

from repository.tournament_repository import TournamentRepository
from schema.tournament_schema import TournamentCreateSchema, TournamentInsertSchema
from schema.user_schema import UserSchema
from service.base_service import BaseService


class TournamentService(BaseService):
    def __init__(self, tournament_repository: TournamentRepository):
        self.tournament_repository = tournament_repository
        super().__init__(tournament_repository)

    def create_tournament(
        self,
        tournament: TournamentCreateSchema,
        current_user: UserSchema,
    ):
        now = datetime.datetime.now(tz=datetime.UTC)

        if tournament.time_finish < now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Finish date cannot be in the past!",
            )

        if tournament.time_start < now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Starting date cannot be in the past!",
            )

        if tournament.time_finish < tournament.time_start:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Finish date cannot be earlier than starting one!",
            )

        if tournament.max_number_of_participants < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Minimum number of participants is 2",
            )

        new_record = TournamentInsertSchema(
            **tournament.model_dump(),
            organizer_id=current_user.id,
        )

        return self.tournament_repository.create(new_record)
