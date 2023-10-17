from fastapi import HTTPException, status

from core.security import (
    create_access_token,
    decode_jwt,
    get_hash_password,
    verify_password,
)
from repository.user_repository import UserRepository
from schema.auth_schema import Payload, Token
from schema.user_schema import (
    UserCreateSchema,
    UserLoginSchema,
    UserRegisterSchema,
    UserSchema,
)
from service.base_service import BaseService
from util.str_operations import str_empty


class AuthService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    def sign_in(self, data: UserLoginSchema):
        found_user = self.user_repository.get_by_email(data.username)
        if not found_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        found_user = found_user.__dict__
        user_hashed_password = found_user.get("password")
        form_password = data.password

        if not verify_password(form_password, user_hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        payload = Payload(
            obj_id=found_user["obj_id"],
            first_name=found_user["first_name"],
            last_name=found_user["last_name"],
            email=found_user["email"],
        )

        access_token = create_access_token(payload)

        result = {
            "access_token": access_token,
            "user_info": payload,
            "token_type": "bearer",
        }
        return result

    # # TODO: Password validation
    # # TODO: Email validation
    def sign_up(self, data: UserRegisterSchema):
        data.model_validate(data)

        db_user = self.user_repository.get_by_email(data.email)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        hashed_password = get_hash_password(data.password)

        user_to_insert = UserCreateSchema(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password=hashed_password,
        )

        db_user = self.user_repository.create(user_to_insert)

        delattr(db_user, "password")

        return db_user

    def get_user_from_token(self, token: Token):
        return decode_jwt(token)
