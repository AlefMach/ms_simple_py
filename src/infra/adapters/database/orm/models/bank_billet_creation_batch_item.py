from sqlalchemy import JSON, Column, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infra.adapters.database.orm.models.entity_model_base import EntityModelBase


class BankBilletCreationBatchItem(EntityModelBase):
    __tablename__ = 'bank_billet_creation_batches_items'

    bank_billet_creation_batch_id: Mapped[int] = mapped_column()
    external_id: Mapped[int] = mapped_column()
    status: Mapped[str] = mapped_column(String(255))
    financial_installment_id: Mapped[int] = mapped_column()
    content = Column(JSON, nullable=False)
    description: Mapped[str] = mapped_column(String(255))

    def __repr__(self):
        return (
            f'<BankBilletCreationBatchItem(id={self.id}, bank_billet_batch_id="{self.bank_billet_creation_batch_id}", '
            f'external_id={self.external_id}), status="{self.status}", '
            f'financial_installment_id="{self.financial_installment_id}", '
            f'content={self.content}, description={self.description}>'
        )
