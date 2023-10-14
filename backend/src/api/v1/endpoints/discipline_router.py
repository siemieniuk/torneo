from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from core.container import Container
from schema.disciplines_schema import DisciplineSchema
from service.discipline_service import DisciplineService

router = APIRouter(prefix="/discipline", tags=["discipline"])


@router.get("")
@inject
async def get_disciplines(
    discipline_service: DisciplineService = Depends(
        Provide[Container.discipline_service]
    ),
):
    return discipline_service.read_all()
