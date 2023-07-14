import logging
from asyncio import current_task
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session

from src.settings import Env, get_settings, is_env

_CONNECT_ARGS_SQLITE = {'check_same_thread': False}

logger = logging.getLogger(__name__)


def _get_async_uri():
    if is_env(Env.UNITTEST):
        return get_settings().database_settings.database_unittest_async_uri

    return get_settings().database_settings.database_async_uri


def _create_async_engine():
    if is_env(Env.UNITTEST):
        return create_async_engine(
            _get_async_uri(),
            connect_args=_CONNECT_ARGS_SQLITE,
        )
    return create_async_engine(
        _get_async_uri(),
        pool_size=get_settings().database_settings.database_pool_size,
        max_overflow=get_settings().database_settings.database_max_overflow,
        pool_pre_ping=True,
        pool_recycle=get_settings().database_settings.database_pool_recicle_seconds,
        echo=get_settings().database_settings.database_echo_sql,
    )


async_engine = _create_async_engine()

AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, autoflush=False, autocommit=False, expire_on_commit=False, future=True
)


@asynccontextmanager
async def get_session():
    """
    Get repositories session from factory and factory will do rollback if an exception are raised and always will
    remove session from registry.
    """
    _async_scoped_session: scoped_session = async_scoped_session(
        session_factory=AsyncSessionLocal, scopefunc=current_task
    )
    try:
        yield _async_scoped_session()
        await _async_scoped_session.commit()
    except Exception as ex:
        logger.error('roolback session caused by: %s', repr(ex))
        await _async_scoped_session.rollback()
        raise
    finally:
        await _async_scoped_session.remove()


@asynccontextmanager
async def get_connection():
    """
    Get connection from engine and engine will do rollback if an exception are raised.
    """
    async with async_engine.connect() as connection:
        async with connection.begin():
            yield connection
