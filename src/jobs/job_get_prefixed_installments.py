import asyncio

from src.infra.adapters.database.orm.settings import get_session
from src.infra.adapters.repositories.financial_installment import RepositoryFinancialInstallment
from src.services.financial_installment import ServiceFinancialInstallment


async def job_get_prefixed_installments():
    async with get_session() as session:
        repository = RepositoryFinancialInstallment(session=session)

        return await ServiceFinancialInstallment(repository=repository).send_installment_to_()


if __name__ == '__main__':
    asyncio.run(job_get_prefixed_installments())
