from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TournamentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    time_start: datetime
    time_finish: datetime
    max_number_of_participants: int
    discipline_id: int
    organizer_id: int
    sponsor_id: int | None


class TournamentUpdateSchema(BaseModel):
    name: str | None
    time_start: datetime | None
    time_finish: datetime | None
    discipline_id: int | None
    sponsor_id: int | None


class TournamentCreateSchema(BaseModel):
    name: str
    time_start: datetime
    time_finish: datetime
    max_number_of_participants: int
    discipline_id: int


class TournamentInsertSchema(TournamentCreateSchema):
    organizer_id: int
