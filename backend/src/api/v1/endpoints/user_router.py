from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_pagination import Page

from core.container import Container
from schema.user_schema import UserSchema
from service.user_service import UserService

router = APIRouter(prefix="/user", tags=["auth"])


@router.get("/")
@inject
def get_all_users(
    service: UserService = Depends(Provide[Container.user_service]),
) -> Page[UserSchema]:
    return service.read_paginated()


@router.get("/{obj_id}")
@inject
def get_user_by_id(
    obj_id: int,
    service: UserService = Depends(Provide[Container.user_service]),
) -> UserSchema:
    return service.read_by_id(obj_id)
