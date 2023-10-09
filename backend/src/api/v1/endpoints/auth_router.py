from datetime import timedelta
from typing import Annotated

import schema as schemas
from core.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from model import models as models
from service.user_service import *
from util.str_operations import str_empty

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/")
async def hello_world():
    return {"message": "Hello Auth"}


@router.post("/token")
async def login(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: SessionLocal = Depends(get_db),
):
    email = data.username
    password = data.password
    user = authenticate_user(email, password, db)
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
    access_token = manager.create_access_token(data={"sub": email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# TODO: Password validation
# TODO: Email validation
@router.post("/register")
async def register_user(user: schemas.UserCreate, db: SessionLocal = Depends(get_db)):
    if str_empty(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required",
        )

    db_user = get_user_by_email(user.email, db)
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

    db_user = create_user(user, db)

    return status.HTTP_201_CREATED


@router.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user=Depends(manager)) -> schemas.User:
    return current_user
