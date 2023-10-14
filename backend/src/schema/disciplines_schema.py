from pydantic import BaseModel


class DisciplineSchema(BaseModel):
    name: str
