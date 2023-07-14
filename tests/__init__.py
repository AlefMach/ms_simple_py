import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text

import src.constants
from src.infra.adapters.database.orm.models.base import BaseModel
from src.infra.adapters.database.orm.settings import get_connection
from src.infra.adapters.logging.settings import set_up_logger
from src.settings import Env, get_settings, is_env

set_up_logger()


async def _execute_upgrade():
    config_path = f'{Path(__file__).resolve().parent.parent}{os.sep}{src.constants.ALEMBIC_INI_FILE}'
    cfg = Config(config_path)
    cfg.set_main_option(
        'script_location',
        f'{Path(__file__).resolve().parent.parent}{os.sep}{src.constants.ALEMBIC_INI_SCRIPT_LOCATION}',
    )
    cfg.set_main_option(
        'version_locations',
        f'{Path(__file__).resolve().parent.parent}{os.sep}{src.constants.ALEMBIC_INI_VERSION_LOCATIONS}',
    )
    command.upgrade(cfg, 'heads')


async def _delete_schema() -> None:
    async with get_connection() as connection:
        result = await connection.execute(text(src.constants.CHECK_SCHEMA_SQL))

        if result.first().result:
            await connection.execute(text(src.constants.DROP_SCHEMA))
        await connection.execute(text(src.constants.CREATE_SCHEMA))


async def create_test_database():
    if is_env(Env.UNITTEST):
        sync_engine_unittest = create_engine(
            get_settings().database_settings.database_unittest_sync_uri, connect_args={'check_same_thread': False}
        )
        BaseModel.metadata.drop_all(bind=sync_engine_unittest)
        BaseModel.metadata.create_all(bind=sync_engine_unittest)

    else:
        try:
            await _delete_schema()
            await _execute_upgrade()
        except Exception as ex:
            raise ex


base_url = 'http://localhost'
