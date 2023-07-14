# Background Tasks

```
src/services/tasks.py
```
```python
import asyncio
import logging
from typing import Optional

logger = logging.getLogger(__name__)


async def send_email_background(sender_email: Optional[str], message: str) -> None:
    """Fake email sender (sleep for 15 seconds).
    :param: sender_email: email address
    :param: message: message to send

    :return: None
    """
    await asyncio.sleep(15)

    logger.info('Email sent successfully - Sender=%s - Message=%s', sender_email, message)

```
```
src/schemas/email.py
```
```python
from typing import Optional
from fastapi_camelcase import CamelModel
from pydantic import validator

class Email(CamelModel):
    sender_email: Optional[str] = ''
    message: str

    @validator('sender_email')
    def validate_sender_email(cls, value):
        """Validate the sender_email
        :param: value: the sender_email to validate

        :return: the sender_email or add some fake email
        """
        # TODO implement validate
        return value or 'fakeemail@xpto.com.br'
```
```
src/entrypoints/routes/v1/partner.py
```
```python
from fastapi import APIRouter
from starlette.background import BackgroundTasks

from src.services import tasks
from src.schemas.email import Email
from src.schemas.schema_base import DefaultResponse

router = APIRouter()


@router.post(
    '/send_email', summary='Send fake email - Use BackgroundTasks', response_model=DefaultResponse, status_code=202
)
async def email(data: Email, background_tasks: BackgroundTasks):
    """You can define background tasks to be run after returning a response.

       BackgroundTasks runs in the same event loop that serves your app's requests.

       https://fastapi.tiangolo.com/tutorial/background-tasks/

    * **param**: data: Email data payload
    * **param**: background_tasks: background tasks object

    **return**: DefaultResponse
    """
    background_tasks.add_task(tasks.send_email_background, sender_email=data.sender_email, message=data.message)

    return DefaultResponse(data=[{'message': 'Email sent in the background'}])
```
