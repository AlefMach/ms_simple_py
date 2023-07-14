import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/', summary='Welcome to the billing-microservice API')
async def welcome() -> str:
    return 'Welcome to billing-microservice-example API. For further information, read the documentation in /docs.'
