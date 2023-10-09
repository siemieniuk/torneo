from backend.database import SessionLocal


class DBSessionMixin:
    def __init__(self, db: SessionLocal) -> None:
        pass


class AppService(DBSessionMixin):
    pass


class AppCRUD(DBSessionMixin):
    pass
