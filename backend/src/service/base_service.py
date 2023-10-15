from typing import Type

from repository.base_repository import BaseRepository


class BaseService:
    def __init__(self, repository: Type[BaseRepository]) -> None:
        self._repository = repository

    def create(self, schema):
        return self._repository.create(schema)

    def read_by_id(self, obj_id: int):
        return self._repository.read_by_id(obj_id)

    def read_all(self):
        result = self._repository.read_all()
        return result

    def read_paginated(self, ):
        return self._repository.read_paginated()

    def update(self, obj_id: int, schema):
        return self._repository.update(obj_id, schema)

    def delete(self, obj_id: int):
        return self._repository.delete(obj_id)
