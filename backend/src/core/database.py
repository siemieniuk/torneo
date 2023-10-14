import csv
from contextlib import AbstractContextManager, contextmanager
from typing import Callable

from sqlalchemy import Engine, create_engine, event, insert
from sqlalchemy.orm import Session, declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

Base = declarative_base()


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class Database:
    def __init__(self, db_url: str):
        self._engine = create_engine(
            db_url,
            connect_args={"check_same_thread": False},
            echo=True,
            pool_timeout=10,
        )

        self._session_factory = sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine
        )

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        db: Session = self._session_factory()
        print(type(db))
        try:
            yield db
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
