from datetime import datetime

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.infra.adapters.database.orm.models.entity_model_base import EntityModelBase


class Payment(EntityModelBase):
    __tablename__ = 'payments'

    financial_installment_id: Mapped[int] = mapped_column()
    external_id: Mapped[str] = mapped_column(String(255))
    issued_at: Mapped[datetime] = mapped_column()
    paid_at: Mapped[datetime] = mapped_column()
    paid_amount: Mapped[int] = mapped_column()
    status: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))  # noqa VNE003
    provider: Mapped[str] = mapped_column(String(255), nullable=False)
    tags: Mapped[str] = Column(Text)
    amount_installment_payable: Mapped[int] = mapped_column()
    total_amount: Mapped[int] = mapped_column()
    overpaid_amount: Mapped[int] = mapped_column()
    discount_amount: Mapped[int] = mapped_column()
    interest_amount: Mapped[int] = mapped_column()

    financing_id: Mapped[int] = mapped_column()

    def __repr__(self):
        return (
            f'<FinancialInstallment(id={self.id}, financial_installment_id={self.financial_installment_id}, '
            f'external_id="{self.external_id}", issued_at="{self.issued_at}", '
            f'status="{self.status}", paid_at="{self.paid_at}", type="{self.type}", tags={self.tags}, '
            f'amount_installment_payable={self.amount_installment_payable}, total_amount={self.total_amount}, '
            f'overpaid_amount={self.overpaid_amount}, '
            f'paid_amount={self.paid_amount}), provider="{self.provider}", discount_amount={self.discount_amount}, '
            f'interest_amount={self.interest_amount}), financing_id={self.financing_id})>'
        )
