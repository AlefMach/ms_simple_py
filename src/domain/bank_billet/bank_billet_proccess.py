import logging
from dataclasses import dataclass
from typing import Optional

from src.domain.bank_billet.use_cases.build_payload_for_create_billet import BuildPayload
from src.infra.adapters.acl.acl_create_billet import CreateBilletRequest
from src.infra.adapters.database.orm.models.bank_billet_creation_batch_item import BankBilletCreationBatchItem
from src.infra.adapters.database.orm.settings import get_session
from src.infra.adapters.repositories.bank_billet_creation_batch_item import RepositoryBankBilletCreationBatchItem
from src.infra.adapters.repositories.financial_installment import RepositoryFinancialInstallment
from src.services.exceptions import SQLAlchemyException

logger = logging.getLogger(__name__)


@dataclass
class CreateBillet:
    installment_id: int
    batch_id: int

    async def handle_create_billet(self) -> dict:
        async with get_session() as session:
            database = RepositoryFinancialInstallment(session)
            result_query_as_dict = await database.get_financial_installment_by_id(self.installment_id)

        payload = await BuildPayload(
            financial_installments=result_query_as_dict.get('financial_installments', None),
            financings=result_query_as_dict.get('financings', None),
        ).build_payload_for_create_billet()

        response = await CreateBilletRequest().create_billet(payload)

        logger.info(
            f'Response for creation billet for id financial installment: {self.installment_id}, '  # noqa G004
            f'Response: {response.get("content")}'  # noqa G004
        )

        await SaveInfoBillet(
            content=response.get('content'),
            status_code=response.get('status_code'),
            batch_id=self.batch_id,
            installment_id=self.installment_id,
        ).handle_save_batch_items()

        return response


@dataclass
class SaveInfoBillet:
    content: dict
    status_code: int
    batch_id: Optional[int]
    installment_id: Optional[int]

    async def handle_save_batch_items(self) -> None:
        if self.status_code == 201:
            await self.save_batch_items(
                external_id=self.content.get('id'), status='done', description=self.content.get('description')
            )
        else:
            if self.content.get('erros'):
                errors = self.content.get('erros')
                description = f'{errors}'
            else:
                errors = self.content.get('detail')
                description = f'{errors}'

            await self.save_batch_items(status='failed', description=description)

    async def save_batch_items(self, external_id=None, status=None, description=None):
        try:
            async with get_session() as session:
                database = RepositoryBankBilletCreationBatchItem(session)
                await database.save(
                    BankBilletCreationBatchItem(
                        bank_billet_creation_batch_id=self.batch_id,
                        external_id=external_id,
                        status=status,
                        description=description,
                        financial_installment_id=self.installment_id,
                        content=self.content,
                    )
                )

        except SQLAlchemyException as err:
            logger.error(
                f'Erro ao tentar salvar info no banco, installment_id: {self.installment_id}, erro: {err}'  # noqa G004
            )
