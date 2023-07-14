from typing import Any, Optional

from fastapi import Query
from fastapi_camelcase import CamelModel
from pydantic import Field


class DefaultResponse(CamelModel):
    data: list[Any] = Field(..., description='Objetos retornados')


class PaginateResponse(DefaultResponse):
    count: int = Field(..., description='Quantidade total de objetos')


class PaginateQuery(CamelModel):
    limit: Optional[int] = Query(None, description='Quantidade máxima de objetos que devem ser retornados')
    offset: Optional[int] = Query(
        None, description='Número que identifica a partir de qual objeto deve comecar a contar'
    )
    sort: str = Query(
        default='id:desc',
        examples={'created_at:desc', 'updated_at:desc'},
        description='Coluna(s) de ordenação dos objetos',
    )
