import abc
from typing import Any, Dict, List, Optional, Type

from src.infra.adapters.database.orm.models.entity_model_base import EntityModelBase
from src.schemas.schema_base import PaginateQuery


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    async def get_all(self, query: PaginateQuery = None) -> List[tuple[Any]]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_id(self, model_id: int) -> Type[EntityModelBase] | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def find_by_id(self, model_id: int) -> tuple[Any] | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def save(self, model) -> EntityModelBase:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, model_id: int, values: Dict[str, Any]) -> tuple[Any] | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, model: Optional[Type[EntityModelBase]]) -> None:
        raise NotImplementedError
