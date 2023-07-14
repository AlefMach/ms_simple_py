# Services

```
src/services/partner.py
```
```python
from dataclasses import dataclass, field
from typing import Any, List, Optional, Type

from src.infra.adapters.database.orm.models import PartnerExample
from src.infra.adapters.repositories.partner import RepositoryPartner
from src.schemas.partner import Partner, PartnerCreate, PartnerUpdate
from src.schemas.schema_base import PaginateQuery
from src.services.service_base import ServiceBase, try_query_except


@dataclass
class Service(ServiceBase):
    repository: RepositoryPartner
    sender_email: str = field(init=False)

    @try_query_except
    async def get_partner_by_id(self, partner_id: int) -> Optional[Type[PartnerExample]]:
        """Find partner for the given id
        :param partner_id: partner id

        :return: PartnerExample
        :raises NotFoundException or SQLAlchemyException
        """
        return await self.repository.get_by_id(partner_id)

    @try_query_except
    async def get_partner_by_document(self, document: str) -> PartnerExample:
        """Find partner for the given document
        :param document: document to find the partner

        :return: Partner
        :raises NotFoundException or SQLAlchemyError
        """
        partner = await self.repository.find_partner_by_document(document)
        if partner:
            partner = Partner.from_orm(partner)
        return self.query_result(result=partner)

    @try_query_except
    async def get_all_partner(self, query: PaginateQuery = None) -> List[tuple[Any]]:
        """Find partner for the given query
        :param query:

        :return: List[PartnerExample]
        :raises NotFoundException or SQLAlchemyError
        """
        partners, total = await self.repository.get_all(query=query)
        if partners:
            partners = [Partner.from_orm(partner) for partner in partners]
        return partners, total

    @try_query_except
    async def create_partner(self, schema: PartnerCreate) -> PartnerExample:
        """Create partner
        :param schema: PartnerCreate

        :return: new PartnerExample
        :raises UniqueException or SQLAlchemyException
        """
        partner = PartnerExample(
            document=schema.document,
            name=schema.name,
            active=schema.active,
            business_address=schema.business_address,
        )

        partner = await self.repository.save(partner)

        return Partner.from_orm(partner)

    @try_query_except
    async def update_partner(self, schema: PartnerUpdate) -> tuple[Any]:
        """Update partner
        :param schema: PartnerUpdate

        :return: PartnerExample updated
        :raises UniqueException or SQLAlchemyException
        """
        values = schema.dict()
        del values['id']

        await self.repository.update(schema.id, values)
        partner = await self.repository.get_by_id(model_id=schema.id)
        return self.query_result(result=partner)

    @try_query_except
    async def delete_partner(self, partner_id: int) -> None:
        """Delete a partner
        :param partner_id: partner id

        :return: None
        :raises SQLAlchemyException
        """
        partner = await self.get_partner_by_id(partner_id)
        await self.repository.delete(partner)

```
