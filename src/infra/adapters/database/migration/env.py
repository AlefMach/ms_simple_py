import asyncio
from concurrent.futures import ThreadPoolExecutor

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from src.infra.adapters.database.orm.models.base import BaseModel
from src.settings import get_settings

target_metadata = BaseModel.metadata


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_async_engine(get_settings().database_settings.database_async_uri, pool_pre_ping=True)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


try:
    asyncio.get_running_loop()
    # we need to create a separate thread so we can block before returning
    with ThreadPoolExecutor(1) as pool:
        result = pool.submit(lambda: asyncio.run(run_migrations_online())).result()
except RuntimeError:
    # no event loop running
    result = asyncio.run(run_migrations_online())
