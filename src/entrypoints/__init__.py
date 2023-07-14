from fastapi import APIRouter

from src.entrypoints.routes import api_router, start
from src.entrypoints.routes.health_check import router as router_health_check

router = APIRouter()
router.include_router(router_health_check, tags=['Health'])
router.include_router(start.router, tags=['Welcome'])
router.include_router(api_router)
