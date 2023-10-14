from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from model import models
from repository.base_repository import BaseRepository


class DisciplineRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, models.Discipline)
