from fastapi import APIRouter

from src.entrypoints.routes.v1.installments import router as router_installments

router = APIRouter()
router.include_router(router_installments, prefix='/installments', tags=['installments'])
