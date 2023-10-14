from pydantic import BaseModel, ConfigDict, EmailStr, model_validator


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    email: EmailStr


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserRegisterSchema(UserLoginSchema):
    password2: str
    first_name: str
    last_name: str

    @model_validator(mode="after")
    def check_passwords_match(self):
        pass2 = self.password2
        pass1 = self.password
        if pass1 != pass2:
            raise ValueError("Passwords do not match")
        return self


class UserCreateSchema(UserSchema):
    password: str


class UserInDB(UserSchema):
    password: str
    disabled: bool | None = None
