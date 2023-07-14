from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from src.infra.adapters.database.orm.models.base import BaseModel


class EntityModelBase(BaseModel):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # noqa VNE003
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
