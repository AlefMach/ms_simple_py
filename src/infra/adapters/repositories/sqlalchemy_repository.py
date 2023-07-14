from typing import Any, Dict, List, Optional, Type

from sqlalchemy import Select, asc, delete, desc, func, update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from src.constants import DEFAULT_OFFSET, DEFAULT_SORT_COLUMN, DEFAULT_SORT_TYPE, ORDER_BY_ASC, ORDER_BY_DESC
from src.infra.adapters.database.orm.models.entity_model_base import EntityModelBase
from src.infra.adapters.repositories.abstract_repository import AbstractRepository
from src.schemas.schema_base import PaginateQuery
from src.settings import get_settings


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session_db = session
        self.entity_model = EntityModelBase

    async def _set_order_by(self, stmt: Select, sort: str):
        """
        :param stmt: Statement in which the ordering will be added.
        :param sort: You must use the pattern column_name:asc or desc, separated by a comma for more than one column.
        """
        if not sort:
            return stmt

        columns_and_orders = {
            column_orders.split(':')[0]: column_orders.split(':')[1]
            for column_orders in sort.split(',')
            if len(column_orders.split(':')) > 1
        } or {DEFAULT_SORT_COLUMN: DEFAULT_SORT_TYPE}

        columns = self.entity_model.__table__.columns

        for column, order in columns_and_orders.items():
            if column in columns:
                if ORDER_BY_DESC == order:
                    stmt = stmt.order_by(desc(column))
                elif ORDER_BY_ASC == order:
                    stmt = stmt.order_by(asc(column))

        return stmt

    async def _get_page(self, stmt: Select, limit: int = None, offset: int = None):
        """
        O objetivo deste método é executar o select e um count da subquery na base e retornar um tupla com os items e qtd_total_items
        :param stmt: Statement in which the limit and offset will be added.
        :param: offset: Number of pagna to offset.
        :param: limit: Number of items to fetch.
        """
        stmt = stmt.offset(offset or DEFAULT_OFFSET).limit(
            min(limit, get_settings().database_settings.database_page_size)
            if limit
            else get_settings().database_settings.database_page_size
        )

        result = await self.session_db.execute(statement=stmt)

        items = result.scalars().all()
        stmt_count = select(func.count()).select_from(stmt.order_by(None).offset(None).limit(None).subquery())

        result = await self.session_db.execute(statement=stmt_count)
        qtd_total_items = result.scalars().one()

        return items, qtd_total_items

    async def get_all(self, query: PaginateQuery = None) -> List[tuple[Any]]:
        """Get all item from database
        :param: query: paginate query params

        :return: List[tuple[Any]]
        """
        if not query:
            query = PaginateQuery()
        statement = select(self.entity_model)
        statement = await self._set_order_by(stmt=statement, sort=query.sort)
        items, qtd_total_items = await self._get_page(stmt=statement, limit=query.limit, offset=query.offset)
        return items, qtd_total_items

    async def get_by_id(self, model_id: int) -> Type[EntityModelBase] | None:
        """Get item by id
        :param: model_id: ID of the model

        :return: EntityModelBase or None
        :raises ``sqlalchemy.repositories.exc.NoResultFound´´ or ``sqlalchemy.repositories.exc.MultipleResultsFound``
        """
        statement = select(self.entity_model).where(self.entity_model.id == model_id)
        results = await self.session_db.execute(statement=statement)
        (result,) = results.one()
        return result

    async def find_by_id(self, model_id: int) -> tuple[Any] | None:
        """Find first item by id
        :param: model_id: ID of the model

        :return: tuple[Any] or None
        """
        statement = select(self.entity_model).where(self.entity_model.id == model_id)
        results = await self.session_db.execute(statement=statement)
        result = results.one_or_none()
        if result:
            (result,) = result
        return result

    async def save(self, model) -> EntityModelBase:
        """Save BaseModel into database
        :param: model: Model to save

        :return: Refresh model object
        """
        self.session_db.add(model)

        await self.session_db.flush()

        return model

    async def update(self, model_id: int, values: Dict[str, Any]) -> tuple[Any] | None:
        """Update BaseModel in database
        :param model_id: ID of the model
        :param values: Dictionary values of the model to be updated

        :return: None
        """
        statement = (
            update(self.entity_model)
            .where(self.entity_model.id == model_id)
            .values(**values)
            .execution_options(synchronize_session='fetch')
        )
        await self.session_db.execute(statement=statement)
        await self.session_db.flush()

    async def delete(self, model: Optional[Type[EntityModelBase]]) -> None:
        """Delete row from database
        :param model: BaseModel to delete

        :return: None
        """
        statement = delete(self.entity_model).where(self.entity_model.id == model.id)
        await self.session_db.execute(statement=statement)
        await self.session_db.flush()
