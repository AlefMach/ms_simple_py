from unittest.mock import MagicMock

import pytest

from src.common.decorators import acache

pytestmark = pytest.mark.asyncio


async def test_decorator_async_cache_should_return_first_result():
    mock = MagicMock()
    mock.side_effect = [1, 10]

    @acache(seconds=10)
    async def func():
        return mock()

    first_result = await func()
    second_result = await func()

    assert first_result == second_result == 1  # not 10


async def test_decorator_async_cache_should_use_cache():
    mock = MagicMock()

    @acache(seconds=10)
    async def func():
        return mock()

    await func()
    await func()

    assert mock.call_count == 1


async def test_decorator_async_cache_should_expire_cache():
    mock = MagicMock()

    @acache(seconds=0)
    async def func():
        return mock()

    await func()
    await func()

    assert mock.call_count == 2


async def test_decorator_async_cache_with_different_params_should_not_use_cache():
    mock = MagicMock()

    @acache(seconds=10)
    async def func(p):
        return mock()

    await func(1)
    await func(2)

    assert mock.call_count == 2
