from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from core.dependencies import get_current_active_user

import schema as schemas
from core.container import Container
from model import models as models
from schema.user_schema import UserSchema
from service.auth_service import AuthService
from service.user_service import *

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/")
async def hello_world():
    return {"message": "Hello Auth"}


@router.post("/token")
@inject
async def login(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    return service.sign_in(data)


@router.post("/register", status_code=status.HTTP_201_CREATED)
@inject
async def register_user(
    data: schemas.UserRegisterSchema,
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    return service.sign_up(data)


# TODO: Fix Pydantic schema User (or replace with other)
@router.get("/me", response_model=UserSchema)
@inject
async def get_me(current_user: UserSchema = Depends(get_current_active_user)):
    return current_user