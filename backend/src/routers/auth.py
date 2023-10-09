from datetime import timedelta
from typing import Annotated

import schemas as _schemas
from algorithms.str_operations import str_empty
from backend.config import ACCESS_TOKEN_EXPIRE_MINUTES
from backend.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from services.auth import (
    authenticate_user,
    create_access_token,
    create_user,
    get_current_active_user,
    get_user,
)
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/")
async def hello_world():
    return {"message": "Hello Auth"}


@router.post("/token")
async def login_for_access_token(
    response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = create_access_token(
    #     data={"sub": user.username}, expires_delta=access_token_expires
    # )
    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# TODO: Password validation
# TODO: Email validation
@router.post("/register")
async def register_user(user: _schemas.UserCreate):
    if str_empty(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required",
        )

    db_user = get_user(user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )

    if user.password != user.password2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )

    db_user = create_user(user)

    return status.HTTP_201_CREATED


@router.get("/users/me", response_model=_schemas.User)
async def read_users_me(
    current_user: Annotated[_schemas.User, Depends(get_current_active_user)]
) -> _schemas.User:
    return current_user
