import json

import httpx

from src.settings import get_settings


class CreateBilletRequest:
    def __init__(self):
        settings = get_settings()
        self.base_url = f'{settings.broker_settings.any_api_external}'

    async def create_billet(self, content: dict) -> dict:
        async with httpx.AsyncClient(base_url=self.base_url, follow_redirects=True) as client:
            response = await client.post('/xpto', json=content)
            json_obj = json.loads(response.content)
            return {'content': json_obj, 'status_code': response.status_code}
