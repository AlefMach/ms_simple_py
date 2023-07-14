from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.infra.adapters.database.orm.models.entity_model_base import EntityModelBase


class Financing(EntityModelBase):
    __tablename__ = 'financings'

    project_amount: Mapped[int] = mapped_column()
    identifier: Mapped[str] = mapped_column(String(255))
    issued_date: Mapped[datetime] = mapped_column(nullable=True)
    registration_fee: Mapped[str] = mapped_column(String(255))
    iof: Mapped[int] = mapped_column()
    interest_fee: Mapped[int] = mapped_column()
    cet: Mapped[str] = mapped_column(String(255))
    installments_number: Mapped[int] = mapped_column()
    grace_period: Mapped[int] = mapped_column()
    first_installment_date: Mapped[datetime] = mapped_column(nullable=True)
    last_installment_date: Mapped[datetime] = mapped_column(nullable=True)
    securitization: Mapped[str] = mapped_column(String(255))
    installment_amount: Mapped[int] = mapped_column()
    next_ipca_update: Mapped[datetime] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(String(255))
    renegotiated: Mapped[str] = mapped_column(String(255))
    ipca_type: Mapped[str] = mapped_column(String(255), default='annual')

    customer_id: Mapped[int] = mapped_column()

    def __repr__(self):
        return (
            f'<Financing(id={self.id}, project_amount={self.project_amount}, identifier="{self.identifier}", '
            f'issued_date="{self.issued_date}"), registration_fee="{self.registration_fee}", iof={self.iof}, '
            f'interest_fee={self.interest_fee}), cet="{self.cet}", installments_number={self.installments_number}, '
            f'grace_period={self.grace_period}), first_installment_date="{self.first_installment_date}", '
            f'last_installment_date="{self.last_installment_date}"), securitization="{self.securitization}", '
            f'installment_amount="{self.installment_amount}"), next_ipca_update={self.next_ipca_update}, '
            f'status="{self.status}"), renegotiated="{self.renegotiated}", ipca_type="{self.ipca_type}"), '
            f'customer_id={self.customer_id})>'
        )
