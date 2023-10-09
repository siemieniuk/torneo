from api.v1.endpoints.auth_router import router as auth_router
from api.v1.endpoints.tournament_router import router as tournament_router
from fastapi import APIRouter

api_router = APIRouter()
router_list = [
    auth_router,
    tournament_router,
]

for router in router_list:
    # router.tags = router.tags.append("v1")
    api_router.include_router(router)
