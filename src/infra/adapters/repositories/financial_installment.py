import json

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Type
from sqlalchemy.future import select

from src.infra.adapters.database.orm import Financing
from src.infra.adapters.database.orm.models.financial_installment import FinancialInstallment
from src.infra.adapters.database.orm.models.payment import Payment
from src.infra.adapters.repositories import AbstractRepository
from src.schemas.schema_base import PaginateQuery
from src.infra.adapters.database.orm.models.entity_model_base import EntityModelBase


@dataclass
class FinancialInstallmentPreload:
    __slots__ = [
        'financial_installments',
        'financings',
    ]
    financial_installments: FinancialInstallment
    financings: Financing

    def dict(self):
        return asdict(self)

    def json(self):
        return json.dumps(self.dict())


class RepositoryFinancialInstallment(AbstractRepository):
    def __init__(self, session):
        super().__init__(session)
        self.financial_installment_model = FinancialInstallment
        self.financing_model = Financing
        self.payment = Payment
        self.installment_status = ['opened', 'expired']
        self.financing_status = [
            'active',
            'disabled',
        ]
        self.securitization = [
            'a1',
            'a2',
            'a3'
        ]

    async def get_all(self, query: PaginateQuery = None) -> List[tuple[Any]]:
        raise NotImplementedError

    async def get_by_id(self, model_id: int) -> Type[EntityModelBase] | None:
        raise NotImplementedError

    async def find_by_id(self, model_id: int) -> tuple[Any] | None:
        raise NotImplementedError

    async def save(self, model) -> EntityModelBase:
        raise NotImplementedError

    async def update(self, model_id: int, values: Dict[str, Any]) -> tuple[Any] | None:
        raise NotImplementedError

    async def delete(self, model: Optional[Type[EntityModelBase]]) -> None:
        raise NotImplementedError

    async def find_installments_not_billet(self, future_data) -> FinancialInstallment:
        """Find all installments don't have billet
        :param future_data

        :return: FinancialInstallment
        """
        stmt = (
            select(self.financial_installment_model, self.f)
            .join(self.f, self.financial_installment_model.financing_id == self.f.id)
            .outerjoin(
                self.payment,
                (self.payment.financial_installment_id == self.financial_installment_model.id) & (self.payment.type == 'regular'),
            )
            .where(self.financial_installment_model.status.in_(self.installment_status))
            .where(self.financial_installment_model.expire_on <= future_data)
            .where(self.f.cet == 'PRE_FIXADO')
            .where(self.f.securitization.in_(self.securitization))
            .where(self.f.status.in_(self.financing_status))
            .where(self.payment.id.is_(None))
        )

        result = await self.session_db.execute(stmt)
        return result.scalars().all()

    async def get_financial_installment_by_id(self, financial_installment_id) -> dict:
        """Get financial installment by id
        :param financial_installment_id

        :return: dict
        """

        stmt = (
            select(
                self.financial_installment_model,
                self.financing_model,
            )
            .join(self.financing_model, self.financing_model.id == self.financial_installment_model.financing_id)
            .where(self.financial_installment_model.id == financial_installment_id)
        )

        result = await self.session_db.execute(stmt)
        row = result.one()

        if row:
            return FinancialInstallmentPreload(
                financial_installments=row[0],
                kobana_wallets=row[1],
            ).dict()
