import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/healthcheck', summary='API is active?')
async def live() -> dict:
    return {'status': 'alive'}
