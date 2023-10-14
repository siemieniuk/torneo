from fastapi import APIRouter

from api.v1.endpoints.auth_router import router as auth_router
from api.v1.endpoints.tournament_router import router as tournament_router
from api.v1.endpoints.user_router import router as user_router
from api.v1.endpoints.discipline_router import router as discipline_router

api_router = APIRouter()
router_list = [
    auth_router,
    tournament_router,
    user_router,
    discipline_router,
]

for router in router_list:
    # router.tags = router.tags.append("v1")
    api_router.include_router(router)
