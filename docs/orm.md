# Object Relational Mapping (ORM) with sqlalchemy

[Sqlalchemy Official](https://docs.sqlalchemy.org/en/20/)

[ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

[Understanding Python SQLAlchemy’s Session](https://www.pythoncentral.io/understanding-python-sqlalchemy-session/)

* Sqlalchemy Architecture

![Sqlalchemy Arch](images/sqlalchemy/sqla_arch_small.png "Sqlalchemy Arch")
```
src/infra/adapters/database/orm/models/partner.py
```
```python
from sqlalchemy import BOOLEAN, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infra.adapters.database.orm.models.entity_model_base import EntityModelBase


class PartnerExample(EntityModelBase):
    __tablename__ = 'partner_example'

    document: Mapped[str] = mapped_column(String(14), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128))
    active: Mapped[bool] = mapped_column(BOOLEAN(), default=True)
    business_address: Mapped[str] = mapped_column(String(128))

    def __repr__(self):
        return (
            f'<PartnerExample(id={self.id}, document="{self.document}", name="{self.name}", '
            f'active={self.active}), business_address={self.business_address})>'
        )

```
```
src/infra/adapters/database/orm/models/__init__.py
```
```python
from src.infra.adapters.database.orm.models.partner import PartnerExample  # noqa F401
```
