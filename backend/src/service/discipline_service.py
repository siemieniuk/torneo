from repository.discipline_repository import DisciplineRepository
from service.base_service import BaseService


class DisciplineService(BaseService):
    def __init__(self, discipline_repository: DisciplineRepository):
        self.discipline_repository = discipline_repository
        super().__init__(discipline_repository)
