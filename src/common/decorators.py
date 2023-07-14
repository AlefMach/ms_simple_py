import logging
from datetime import datetime, timedelta
from functools import wraps

from async_lru import alru_cache

logger = logging.getLogger(__name__)


def acache(seconds: int, maxsize: int = 128):
    """Decorator to apply cache with expiration time, allows to return the response of the async
    function if it was previously called. It can save time when an expensive or I/O bound function
    is periodically called with the same arguments.

    :param: seconds: expiration time in seconds
    :param: maxsize: maximum size to cache.

    :return: function response
    """

    def wrapper_cache(func):
        func = alru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        async def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime

            logger.debug('Expiration: %s', {func.expiration})
            return await func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache
