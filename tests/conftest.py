import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient

from src.app import app
from tests import create_test_database


@pytest.fixture(scope='session')
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def os_enviroments_database_mock():
    return {
        'DATABASE_HOST': 'test_host',
        'DATABASE_NAME': 'test_database_name',
        'DATABASE_USER': 'test_database_user',
        'DATABASE_PASSWORD': 'test_database_password',
        'DATABASE_POOL_SIZE': '99',
        'DATABASE_POOL_TIMEOUT_SECONDS': '99',
        'DATABASE_MAX_OVERFLOW': '99',
        'DATABASE_POOL_RECICLE_SECONDS': '99',
        'DATABASE_ECHO_SQL': 'debug',
        'PAGE_SIZE': '1',
    }


@pytest.fixture()
def os_enviroments_launch_darkly_mock():
    return {
        'LAUNCH_DARKLY_SECRET_KEY': 'test_secret',
        'LAUNCH_DARKLY_EXAMPLE_FLAG': 'test_flag',
    }


@pytest.fixture()
def os_enviroments_server_mock():
    return {
        'APP_DEFAULT_HOST': 'test_host',
        'APP_DEFAULT_PORT': '8888',
        'HTTP_MAX_CONNECTIONS': '1',
        'WORKERS': '2',
        'ENVIRONMENT': 'test',
    }


@pytest.fixture()
def os_enviroments_log_mock():
    return {
        'LOG_LEVEL': 'INFO',
        'LOG_FORMAT': '{level} | {message}',
    }


@pytest.fixture()
def os_enviroments_otlp_mock():
    return {
        'TEMPO_HOST': '0.0.0.0',
        'OTLP_AGENT_GRPC_PORT': '1111',
        'OTLP_AGENT_HTTP_PORT': '2222',
        'OTLP_AGENT_AUTH_TOKEN': 'test_token',
    }


@pytest.fixture()
def os_enviroments_redis_mock():
    return {
        'REDIS_BASE_URL': '0.0.0.0',
        'REDIS_USER': 'test_user',
        'REDIS_PASS': 'test_pass',
    }


@pytest_asyncio.fixture(scope='function')
async def client() -> AsyncGenerator:
    async with AsyncClient(
        app=app,
        base_url='http://localhost:8000',
        headers={'Content-Type': 'application/json'},
    ) as _client:
        yield _client


@pytest_asyncio.fixture()
async def create_database():
    await create_test_database()
