from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from jose import jwt
from pydantic import ValidationError

from core.config import JWT_ALGORITHM, SECRET_KEY
from core.container import Container
from core.exceptions import AuthException
from core.security import JWTBearer
from model.models import User
from schema.auth_schema import Payload
from service.user_service import UserService


@inject
def get_current_user(
    token: str = Depends(JWTBearer()),
    service: UserService = Depends(Provide[Container.user_service]),
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=JWT_ALGORITHM)
        token_data = Payload(**payload)
    except (jwt.JWTError, ValidationError):
        raise AuthException(detail="Could not validate credentials")

    current_user: User = service.read_by_id(token_data.obj_id)
    if not current_user:
        raise AuthException(detail="User not found")
    return current_user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise AuthException("Inactive user")
    return current_user
