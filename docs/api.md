# API

## Documentation

The API is built with [FastAPI](https://fastapi.tiangolo.com/). To access the local api documentation:

- [http://localhost:8000/docs](http://localhost:8000/docs): useful for interacting with the API;
- [http://localhost:8000/redoc](http://localhost:8000/redoc): better to publish.

```
src/entrypoints/routes/v1/partner.py
```

```python
import logging

from fastapi import APIRouter, Depends

from src.infra.adapters.repositories import get_repository
from src.infra.adapters.repositories.partner import RepositoryPartner
from src.schemas.partner import Email, Partner, PartnerCreate, PartnerUpdate
from src.schemas.schema_base import DefaultResponse, PaginateQuery, PaginateResponse
from src.services.partner import Service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/', summary='Get partners', response_model=PaginateResponse, status_code=200)
async def read_partners(
    query: PaginateQuery = Depends(PaginateQuery),  # noqa B008
    repository: RepositoryPartner = Depends(get_repository(repo_type=RepositoryPartner)),  # noqa B008
):
    """Get partners from database
    * **param**: query: limit, offset and sort parameters
    * **param**: repository: Session of sql database

    **return**: list[Partner]
    """
    partners, total = await Service(repository=repository).get_all_partner(query=query)
    return PaginateResponse(data=partners, count=total)


@router.get('/document/{document}', summary='Get partner by document', response_model=Partner, status_code=200)
async def read_partner_by_document(
    document: str,
    repository: RepositoryPartner = Depends(get_repository(repo_type=RepositoryPartner)),  # noqa B008
):
    """Get partner by document
    * **param**: document: Document of the Partner
    * **param**: session_db: Session of sql database

    **return**: Partner
    """
    return await Service(repository=repository).get_partner_by_document(document)


@router.get('/{partner_id}', summary='Get partner by id', response_model=Partner, status_code=200)
async def read_partner_by_id(
    partner_id: int,
    repository: RepositoryPartner = Depends(get_repository(repo_type=RepositoryPartner)),  # noqa B008
):
    """Get Partner by id
    * **param**: partner_id: ID to find the Partner
    * **param**: session_db: Session of sql database

    **return**: Partner
    """
    return await Service(repository=repository).get_partner_by_id(partner_id)


@router.post('/', summary='Create partner', response_model=DefaultResponse, status_code=201)
async def create_partner(
    data: PartnerCreate,
    repository: RepositoryPartner = Depends(get_repository(repo_type=RepositoryPartner)),  # noqa B008
):
    """Create partner
    * **param**: data: PartnerCreate data payload
    * **param**: session_db: Session of sql database

    **return**: DefaultResponse
    """
    partner = await Service(repository=repository).create_partner(data)

    return DefaultResponse(data=[{'Partner': partner}])


@router.put('/', summary='Update partner', response_model=DefaultResponse, status_code=200)
async def update_partner(
    data: PartnerUpdate,
    repository: RepositoryPartner = Depends(get_repository(repo_type=RepositoryPartner)),  # noqa B008
):
    """Update Partner
    * **param**: data: PartnerUpdate data payload
    * **param**: session_db: Session of sql database

    **return**: DefaultResponse
    """
    partner = await Service(repository=repository).update_partner(data)

    return DefaultResponse(data=[{'Partner': partner}])


@router.delete('/{partner_id}', summary='Delete partner', status_code=204)
async def delete_partner(
    partner_id: int,
    repository: RepositoryPartner = Depends(get_repository(repo_type=RepositoryPartner)),  # noqa B008
):
    """Delete partner
    * **param**: partner_id: Partner id
    * **param**: session_db: Session of sql database

    **return**: None
    """
    await Service(repository=repository).delete_partner(partner_id)


```
```
src/entrypoints/routes/v1/__init__.py
```

```python
from fastapi import APIRouter

from src.entrypoints.routes.v1.partner import router as router_partner

router = APIRouter()
router.include_router(router_partner, prefix='/partners', tags=['partner'])

```

```
src/entrypoints/routes/__init__.py
```

```python
from fastapi import APIRouter

from src.entrypoints.routes.v1 import router as v1_router

api_router = APIRouter()
api_router.include_router(v1_router, prefix='/v1', tags=['partner'])

```

```
src/app.py
```

```python
from src.entrypoints.routes import api_router

_app = ...
_app.include_router(api_router)
```

```
tests/e2e/entrypoints/routes/v1/test_partner.py
```
```python
from datetime import datetime, timezone

import pytest
from httpx import AsyncClient
from sqlalchemy import insert, text

from src.infra.adapters.database.orm.models import PartnerExample
from src.infra.adapters.database.orm.settings import get_connection, get_session
from src.settings import get_settings

@pytest.mark.asyncio()
@pytest.mark.usefixtures('prepare_database')
async def test_read_partners_with_paginacao_in_database_should_return_success_and_json_partners(
    client: AsyncClient,
):
    # arrange
    expected = {
        'data': [
            {
                'name': 'test solar',
                'document': '00623904000173',
                'active': True,
                'businessAddress': 'rua a',
                'id': 1,
            }
        ],
        'count': 1,
    }

    # act
    response = await client.get(
        f'/v1/partners/?limit=100&offset=0'
        f'&sort=created_at:desc'
    )
    # assert
    assert response.status_code == 200
    assert response.json() == expected


@pytest.mark.asyncio()
@pytest.mark.usefixtures('prepare_database')
async def test_read_partners_with_partners_in_database_should_return_success_and_json_partners(
    client: AsyncClient,
):
    # arrange
    expected = {
        'data': [
            {
                'name': 'test solar',
                'document': '00623904000173',
                'active': True,
                'businessAddress': 'rua a',
                'id': 1,
            }
        ],
        'count': 1,
    }

    # act
    response = await client.get('/v1/partners/')
    # assert
    assert response.status_code == 200
    assert response.json() == expected

@pytest.mark.asyncio()
@pytest.mark.usefixtures('prepare_database')
async def test_read_partner_by_id_with_valid_id_should_return_success_and_partner(client: AsyncClient):
    # arrange
    expected = {
        'name': 'test solar',
        'document': '00623904000173',
        'active': True,
        'businessAddress': 'rua a',
        'id': 1,
    }
    # act
    response = await client.get('/v1/partners/1')
    # assert
    assert response.status_code == 200
    assert response.json() == expected


@pytest.mark.asyncio()
@pytest.mark.usefixtures('prepare_database')
async def test_read_partner_by_document_with_document_already_in_database_should_return_success_and_partners(
    client: AsyncClient,
):
    # arrange
    expected = {
        'name': 'test solar',
        'document': '00623904000173',
        'active': True,
        'businessAddress': 'rua a',
        'id': 1,
    }
    document = '00623904000173'
    # act
    response = await client.get(
        f'/v1/partners/document/{document}'
    )
    # assert
    assert response.status_code == 200
    assert response.json() == expected


@pytest.mark.asyncio()
@pytest.mark.usefixtures('prepare_database')
async def test_read_partner_by_document_with_document_not_exist_in_database_should_return_not_content(
    client: AsyncClient,
):
    # arrange
    document = '0062390400017'
    # act
    response = await client.get(
        f'/v1/partners/document/{document}'
    )
    # assert
    assert response.status_code == 204


@pytest.mark.asyncio()
@pytest.mark.usefixtures('prepare_database')
async def test_create_partner_with_same_document_return_error_unique_constraint(client: AsyncClient):
    # arrange
    payload = {'name': 'test solar', 'document': '00623904000173', 'active': True, 'businessAddress': 'rua 1'}
    expected = {'detail': 'Unique constraint - the value already exists in the database'}

    # act
    response = await client.post('/v1/partners/', json=payload)

    assert response.status_code == 422
    assert response.json() == expected


@pytest.mark.asyncio()
async def test_create_partner_with_document_invalid_return_error_message_invalid_cpf(client: AsyncClient):
    # arrange
    payload = {'name': 'test solar', 'document': '00623904000172', 'active': True}
    expected = {'detail': 'Invalid CPF/CNPJ'}

    # act
    response = await client.post('/v1/partners/', json=payload)

    assert response.status_code == 422
    assert response.json() == expected


@pytest.mark.asyncio()
@pytest.mark.usefixtures('prepare_database')
async def test_create_partner_with_document_valid_return_success(client: AsyncClient):
    # arrange
    payload = {'name': 'test solar', 'document': '72610132000146', 'active': True, 'businessAddress': 'Rua a'}

    # act
    response = await client.post('/v1/partners/', json=payload)

    # assert
    assert response.status_code == 201


@pytest.mark.asyncio()
@pytest.mark.usefixtures('prepare_database')
async def test_delete_partner_with_valid_id_return_success(client: AsyncClient):
    # arrange
    _id = 2
    stmt = insert(PartnerExample).values(
        id=_id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        document='09066280000105',
        name='teste partner',
        active=True,
        business_address='rua a',
    )
    async with get_session() as session:
        async with session.begin():
            result = await session.execute(statement=stmt)
            assert result.rowcount == 1
    # act
    response = await client.delete(f'/v1/partners/{_id}')

    # assert
    assert response.status_code == 204


@pytest.mark.asyncio()
@pytest.mark.usefixtures('prepare_database')
async def test_update_partner_with_new_name_return_success(client: AsyncClient):
    # arrange
    dt = datetime.now(timezone.utc)
    _id = 2
    _new_name = 'Any Name'
    async with get_connection() as connection:
        sql = (
            f'INSERT INTO partner_example (id, created_at, updated_at, canceled_at, document, name, active, business_address) '
            f"VALUES('{_id}', '{dt.strftime('%Y-%m-%d %H:%M:%S-00')}', '{dt.strftime('%Y-%m-%d %H:%M:%S-00')}', null, '72610132000146', 'teste partner', true, 'rua a');"  # noqa Q000
        )
        result = await connection.execute(text(sql))
        assert result.rowcount == 1

    payload = {
        'id': _id,
        'name': _new_name,
        'document': '72610132000146',
        'active': True,
        'businessAddress': 'rua a',
    }

    # act
    response = await client.put('/v1/partners/', json=payload)

    # assert
    data = response.json()
    assert response.status_code == 200
    assert data['data'][0]['Partner']['id'] == _id
    assert data['data'][0]['Partner']['name'] == _new_name
```
