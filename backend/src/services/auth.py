from datetime import datetime, timedelta
from typing import Annotated

import models.models as _models
import schemas as _schemas
from backend.config import JWT_ALGORITHM, JWT_SECRET_KEY, oauth2_scheme
from backend.database import SessionLocal, get_db
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select, union

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user(email: str) -> _schemas.UserInDB | None:
    stmt = select(_models.User).where(_models.User.email == email)
    db = next(get_db())
    result = db.execute(stmt).first()
    if result is not None:
        return _schemas.UserInDB(**result)
    return None


# TODO: Get password and use verify_password
def authenticate_user(email: str, password: str):
    stmt = select(_models.User).where(_models.User.email == email)
    db = next(get_db())
    user = db.execute(stmt).scalars().first()

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def create_user(user: _schemas.UserCreate):
    hashed_password = get_hash_password(user.password)
    print(hashed_password)
    new_user = _models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hashed_password,
    )
    db = next(get_db())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# TODO: Return typing
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = _schemas.User(email=email)
    except JWTError:
        raise credentials_exception
    return token_data


# TODO: Return typing
async def get_current_active_user(
    current_user: Annotated[_schemas.User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user
