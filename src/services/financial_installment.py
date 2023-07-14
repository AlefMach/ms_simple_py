import asyncio
import logging
import time
from dataclasses import dataclass, field

from src.common.helpers import DateHelper
from src.domain.installment.uses_cases.installment_creation import send_installment_created_event
from src.infra.adapters.repositories.financial_installment import RepositoryFinancialInstallment
from src.services.service_base import ServiceBase, try_query_except

logger = logging.getLogger(__name__)


@dataclass
class ServiceFinancialInstallment(ServiceBase):
    repository: RepositoryFinancialInstallment

    date_helper: DateHelper = field(default_factory=DateHelper)

    @try_query_except
    async def get_installments_not_billet(self):
        """Find all installments don't have billit

        :return: FinancialInstallment
        :raises NotFoundException or SQLAlchemyException
        """
        return await self.repository.find_installments_not_billet(self.date_helper.future_data())

    @try_query_except
    async def send_installment_to_(self):
        """Loop in installments list and send to kafka for each"""
        start_time = time.time()
        installments = await self.get_installments_not_billet()

        await asyncio.gather(
            *map(  # noqa C417
                lambda installment: send_installment_created_event(installment.id),
                installments,
            )
        )
        
        process_time = round(time.time() - start_time, 10)
        logger.info(f'LATENCY[*] {process_time} s')  # noqa G004
        print('LATENCY', f'[*] {process_time} s')

        return {'Success': True}
