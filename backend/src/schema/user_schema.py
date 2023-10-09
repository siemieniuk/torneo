from pydantic import BaseModel, EmailStr


class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    disabled: bool | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserLogin):
    first_name: str
    last_name: str
    email: EmailStr
    password2: str


class UserInDB(User):
    hashed_password: str
