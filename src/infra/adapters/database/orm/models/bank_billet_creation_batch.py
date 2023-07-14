from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.infra.adapters.database.orm.models.entity_model_base import EntityModelBase


class BankBilletCreationBatch(EntityModelBase):
    __tablename__ = 'bank_billet_creation_batches'

    batch_identifier: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(255))

    def __repr__(self):
        return (
            f'<BankBilletCreationBatch(id={self.id}, status="{self.status}", '
            f'batch_identifier="{self.batch_identifier}">'
        )
