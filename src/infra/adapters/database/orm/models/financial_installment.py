from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.infra.adapters.database.orm.models.entity_model_base import EntityModelBase


class FinancialInstallment(EntityModelBase):
    __tablename__ = 'financial_installments'

    number: Mapped[int] = mapped_column()
    status: Mapped[str] = mapped_column(String(255))
    amount: Mapped[int] = mapped_column()
    expire_on: Mapped[datetime] = mapped_column(nullable=True)
    paid_at: Mapped[datetime] = mapped_column(nullable=True)
    paid_amount: Mapped[int] = mapped_column(default=0)
    provider: Mapped[str] = mapped_column(String(255))
    discount_amount: Mapped[int] = mapped_column(default=0)
    interest_amount: Mapped[int] = mapped_column(default=0)
    securitization: Mapped[str] = mapped_column(String(255), default=None)

    financing_id: Mapped[int] = mapped_column()

    def __repr__(self):
        return (
            f'<FinancialInstallment(id={self.id}, number={self.number}, status="{self.status}", '
            f'amount={self.amount}), expire_on="{self.expire_on}", paid_at="{self.paid_at}", '
            f'paid_amount={self.paid_amount}), provider="{self.provider}", discount_amount={self.discount_amount}, '
            f'interest_amount={self.interest_amount}), financing_id={self.financing_id}), '
            f'securization={self.securitization})>'
        )

    def to_dict(self):
        return {
            'id': self.id,
            'number': self.number,
            'status': self.status,
            'amount': self.amount,
            'expire_on': self.expire_on.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'paid_at': self.paid_at,
            'paid_amount': self.paid_amount,
            'provider': self.provider,
            'discount_amount': self.discount_amount,
            'interest_amount': self.interest_amount,
            'financing_id': self.financing_id,
        }
