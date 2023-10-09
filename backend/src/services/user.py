import models.models as _models
import schemas as _schemas
from main import AppCRUD, AppService
from schemas.user import UserCreate
from sqlalchemy import Select


class UserService(AppService):
    def get_by_username(self, username) -> _schemas.UserInDB | None:
        stmt = Select(_models.User).where(_models.User.username == username)
        result = self.db.execute(stmt).first()
        if result is not None:
            return _schemas.UserInDB(**result)
        return None
