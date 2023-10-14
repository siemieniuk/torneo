from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select

import model.models as _models
import schema as _schemas
from core.config import JWT_ALGORITHM, SECRET_KEY, oauth2_scheme
from repository.user_repository import UserRepository
from service.base_service import BaseService


class UserService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)
