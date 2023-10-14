from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page

from core.container import Container
from core.dependencies import get_current_active_user
from schema.tournament_schema import TournamentCreateSchema, TournamentSchema
from schema.user_schema import UserSchema
from service.tournament_service import TournamentService

router = APIRouter(prefix="/tournament", tags=["tournament"])


@router.post("", status_code=status.HTTP_201_CREATED)
@inject
async def create_tournament(
    tournament: TournamentCreateSchema,
    current_user: UserSchema = Depends(get_current_active_user),
    tournament_service: TournamentService = Depends(
        Provide[Container.tournament_service]
    ),
):
    return tournament_service.create_tournament(tournament, current_user)


@router.get("")
@inject
async def get_paginated_tournaments(
    tournament_service: TournamentService = Depends(
        Provide[Container.tournament_service]
    ),
    # ) -> Page[TournamentSchema]:
) -> Page[TournamentSchema]:
    return tournament_service.read_paginated()


@router.get("/{id}")
@inject
async def get_tournament(
    id: int,
    tournament_service: TournamentService = Depends(
        Provide[Container.tournament_service]
    ),
):
    return tournament_service.read_by_id(id)


# TODO: Verify if user is an organizer
@router.put("/{id}")
@inject
async def update_tournament(
    id: int,
    tournament: TournamentSchema,
    tournament_service: TournamentService = Depends(
        Provide[Container.tournament_service]
    ),
):
    return tournament_service.update(id, tournament)


# TODO: Verify if user is an organizer
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_tournament(
    id: int,
    tournament_service: TournamentService = Depends(
        Provide[Container.tournament_service]
    ),
):
    return tournament_service.delete(id)
