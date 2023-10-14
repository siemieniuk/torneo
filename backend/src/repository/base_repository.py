# TODO: Implement
from contextlib import AbstractContextManager
from typing import Any, Callable, Dict, List

from fastapi import HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.exceptions import NotFoundException


class BaseRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]], model
    ) -> None:
        self.session_factory = session_factory
        self.model = model

    def create(self, schema):
        with self.session_factory() as session:
            query = self.model(**schema.model_dump())
            try:
                session.add(query)
                session.commit()
                session.refresh(query)
            except IntegrityError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Violated costraints",
                )
            return query

    def read_by_id(self, id: int):
        with self.session_factory() as session:
            stmt = select(self.model).where(self.model.id == id)
            result = session.execute(stmt)

            object_in_db = result.scalars().first()

            if not object_in_db:
                raise NotFoundException
            return object_in_db

    def read_all(self, columns: List[str] = None):
        with self.session_factory() as session:
            if columns:
                stmt = select(self.model)
            else:
                stmt = select(self.model.c[*columns])
            result = session.execute(stmt).scalars().all()
            return result

    def read_paginated(self, columns: List[str] = None):
        with self.session_factory() as session:
            if columns:
                stmt = select(self.model)
            else:
                stmt = select(self.model.c[*columns])
            return paginate(session, stmt)

    def update(self, obj_id: int, schema):
        with self.session_factory() as session:
            try:
                stmt = (
                    update(self.model)
                    .where(self.model.id == obj_id)
                    .values(**schema.model_dump(exclude_none=True))
                )
            except IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Violated constraints",
                )
            session.execute(stmt)
            session.commit()
            return self.read_by_id(id)

    def update_attributes(self, obj_id: int, to_update: Dict[str, Any] = None):
        with self.session_factory() as session:
            try:
                stmt = (
                    update(self.model)
                    .where(self.model.id == obj_id)
                    .values(**to_update)
                )
                session.execute(stmt)
                session.commit()
            except Exception:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            return self.read_by_id(id)

    def delete(self, obj_id: int):
        with self.session_factory() as session:
            stmt = delete(self.model).where(self.model.id == obj_id)
            session.execute(stmt)
            session.commit()
