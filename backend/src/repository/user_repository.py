from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

import model.models as _models
from repository.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, _models.User)

    def get_by_email(self, email: str) -> _models.User | None:
        stmt = select(self.model).where(self.model.email == email)

        with self.session_factory() as session:
            result = session.execute(stmt).scalars().first()
            return result
