import logging

from src.domain.eventing.service import EventingService
from src.infra.adapters.repositories.bank_billet_creation_batch import RepositoryBankBilletCreationBatch
from src.services.service_base import try_query_except
from src.infra.adapters.database.orm.models.bank_billet_creation_batch import BankBilletCreationBatch
from src.services.exceptions import SQLAlchemyException
from src.infra.adapters.database.orm.settings import get_session

logger = logging.getLogger(__name__)


@try_query_except
async def send_installment_created_event(installment_id):
    batch = create_bank_billet_creation_batch(installment_id)
    event = EventingService(event='create', installment_id=installment_id, batch_id=batch.id)
    await event.process_event()
    logger.info(f'Sent financial_installment {installment_id} successfully!')  # noqa G004


async def create_bank_billet_creation_batch(installment_id):
    try:
        async with get_session() as session:
            database = RepositoryBankBilletCreationBatch(session)
    
            return await database.save(BankBilletCreationBatch(
                batch_identifier='xptoSomething',
                status='pendding'
            )
        )

    except SQLAlchemyException as err:
        logger.error(
            f'Erro ao tentar salvar info no banco, installment_id: {installment_id}, erro: {err}'  # noqa G004
        )
