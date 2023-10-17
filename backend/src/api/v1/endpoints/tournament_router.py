from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, Response, status
from fastapi.responses import JSONResponse
from fastapi_pagination import Page

from core.container import Container
from core.dependencies import get_current_active_user
from schema.tournament_schema import (
    TournamentCreateSchema,
    TournamentSchema,
    TournamentUpdateSchema,
)
from schema.user_schema import UserSchema
from service.tournament_service import TournamentService
from util.str_operations import str_empty

router = APIRouter(prefix="/tournament", tags=["tournament"])


Page = Page.with_custom_options(size=Query(10, ge=1, le=10))


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
    name: str = "",
    tournament_service: TournamentService = Depends(
        Provide[Container.tournament_service]
    ),
) -> Page[TournamentSchema]:
    if str_empty(name):
        return tournament_service.read_paginated()
    else:
        return tournament_service.read_paginated_by_name(name)


@router.get("/{obj_id}")
@inject
async def get_tournament(
    obj_id: int,
    tournament_service: TournamentService = Depends(
        Provide[Container.tournament_service]
    ),
):
    return tournament_service.read_by_id(obj_id)


@router.put("/{obj_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def update_tournament(
    obj_id: int,
    tournament: TournamentUpdateSchema,
    current_user: UserSchema = Depends(get_current_active_user),
    tournament_service: TournamentService = Depends(
        Provide[Container.tournament_service]
    ),
):
    return tournament_service.update(obj_id, tournament, current_user)


@router.delete("/{obj_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_tournament(
    obj_id: int,
    current_user: UserSchema = Depends(get_current_active_user),
    tournament_service: TournamentService = Depends(
        Provide[Container.tournament_service]
    ),
):
    return tournament_service.delete(obj_id, current_user)
