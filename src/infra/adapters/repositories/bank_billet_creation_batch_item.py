from typing import Any, Dict, List, Optional, Type

from src.infra.adapters.database.orm.models.entity_model_base import EntityModelBase
from src.infra.adapters.repositories import AbstractRepository
from src.schemas.schema_base import PaginateQuery


class RepositoryBankBilletCreationBatchItem(AbstractRepository):
    def __init__(self, session):
        self.session_db = session

    async def get_all(self, query: PaginateQuery = None) -> List[tuple[Any]]:
        raise NotImplementedError

    async def get_by_id(self, model_id: int) -> Type[EntityModelBase] | None:
        raise NotImplementedError

    async def find_by_id(self, model_id: int) -> tuple[Any] | None:
        raise NotImplementedError

    async def save(self, model) -> EntityModelBase:
        """Save BaseModel into database
        :param: model: Model to save

        :return: Refresh model object
        """
        self.session_db.add(model)

        await self.session_db.flush()

        return model

    async def update(self, model_id: int, values: Dict[str, Any]) -> tuple[Any] | None:
        raise NotImplementedError

    async def delete(self, model: Optional[Type[EntityModelBase]]) -> None:
        raise NotImplementedError
