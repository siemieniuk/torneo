from pydantic import BaseModel


class LoginItem(BaseModel):
    username: str
    password: str
