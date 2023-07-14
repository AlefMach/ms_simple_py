import pytest
from httpx import AsyncClient

from src.app import app
from tests import base_url


@pytest.mark.asyncio()
async def test_live():
    # act
    async with AsyncClient(app=app, base_url=base_url) as client:
        response = await client.get('/healthcheck')

    # assert
    assert response.status_code == 200
