import logging
from dataclasses import dataclass

from src.common.helpers.response_helper import failed_response
from src.domain.bank_billet.bank_billet_proccess import CreateBillet
from src.services.service_base import ServiceBase

logger = logging.getLogger(__name__)


@dataclass
class EventingService(ServiceBase):
    event: str
    installment_id: int
    batch_id: int

    async def process_event(self) -> dict:
        try:
            logger.info(f'{self.event} event received = {self.installment_id}')  # noqa G004
            match self.event:
                case 'create':
                    return await CreateBillet(
                        installment_id=self.installment_id, batch_id=self.batch_id
                    ).handle_create_billet()

                case _:
                    return failed_response('Evento não implementado')

        except Exception as err:
            description = (
                f'Erro ao tentar processar evento: {self.event}, '
                f'installment_id: {self.installment_id}, error: {err}'
            )
            logger.error(description)
            return failed_response(description)
