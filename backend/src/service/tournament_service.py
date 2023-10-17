import datetime

from fastapi import HTTPException, status

from repository.tournament_repository import TournamentRepository
from schema.tournament_schema import (
    TournamentCreateSchema,
    TournamentInsertSchema,
    TournamentSchema,
    TournamentUpdateSchema,
)
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
            organizer_id=current_user.obj_id,
        )

        return self.tournament_repository.create(new_record)

    def read_paginated_by_name(self, name: str):
        return self.tournament_repository.read_paginated_by_name(name)

    def update(
        self,
        tournament_id: int,
        tournament: TournamentUpdateSchema,
        user: UserSchema,
    ):
        if not self._is_owner(tournament_id, user):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        db_tournament = self.tournament_repository.update(tournament_id, tournament)
        return db_tournament

    def delete(self, tournament_id: int, user: UserSchema):
        if not self._is_owner(tournament_id, user):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        self.tournament_repository.delete(tournament_id)
        return True

    def _is_owner(self, tournament_id: int, user: UserSchema) -> bool:
        db_tournament = self.tournament_repository.read_by_id(tournament_id)
        db_tournament = TournamentSchema.model_validate(db_tournament)

        return db_tournament.organizer_id == user.obj_id
