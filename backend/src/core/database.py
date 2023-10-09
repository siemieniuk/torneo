# from geoalchemy2 import load_spatialite
from sqlalchemy import create_engine

# from sqlalchemy.event import listen
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

Base = declarative_base()


class Database:
    def __init__(self, db_url):
        self._engine = create_engine(
            SQLALCHEMY_DATABASE_URL,
            connect_args={"check_same_thread": False},
            echo=True,
            pool_timeout=10,
        )

        self._session_factory = sessionmaker(
            autocommit=False, autoflush=False, bind=engine
        )


# listen(engine, "connect", load_spatialite)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True,
    pool_timeout=10,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
