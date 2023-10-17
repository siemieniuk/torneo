from contextlib import AbstractContextManager
from typing import Callable

from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session

from model import models
from repository.base_repository import BaseRepository


class TournamentRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, models.Tournament)

    def read_paginated_by_name(
        self,
        name: str,
    ):
        with self.session_factory() as session:
            stmt = select(self.model).where(self.model.name.like(f"%{name}%"))
            return paginate(session, stmt)
