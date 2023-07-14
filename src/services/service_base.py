import logging
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Optional, Tuple, Type

from fastapi_camelcase import CamelModel
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound, SQLAlchemyError

from src.common.helpers import ExceptionHelper
from src.infra.adapters.repositories.exceptions import DatabaseConnectionRefusedError
from src.services.exceptions import NotFoundException, SQLAlchemyException, UniqueException, ValidationException

logger = logging.getLogger(__name__)


@dataclass
class ServiceBase:
    @classmethod
    def query_result(cls, result: list[Any] | dict[str, Any] | Type[CamelModel] | Optional[Tuple[Any]]) -> Any:
        """Query result, obtain the result or raise an exception"""
        if result:
            return result
        raise NotFoundException()


def try_query_except(func: Callable):
    """Decorator to try to raise an exception"""

    @wraps(func)
    async def wrapped_func(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
        except NoResultFound as exc:
            raise NotFoundException() from exc
        except ValidationError as exc:
            logger.exception(exc)
            exc_info = ExceptionHelper.get_exc_info()
            raise ValidationException(stacktrace=ExceptionHelper.format_exception(exc_info))
        except IntegrityError as exc:
            logger.exception(exc)
            exc_info = ExceptionHelper.get_exc_info()
            raise UniqueException(stacktrace=ExceptionHelper.format_exception(exc_info))
        except SQLAlchemyError as exc:
            logger.exception(exc)
            exc_info = ExceptionHelper.get_exc_info()
            raise SQLAlchemyException(stacktrace=ExceptionHelper.format_exception(exc_info))
        except ConnectionRefusedError as cre:
            logger.error('Database service is not available! %s', repr(cre))
            raise DatabaseConnectionRefusedError(repr(cre)) from cre
        except Exception as ex:
            logger.exception('Unknow error %s', repr(ex))
            raise
        else:
            return result

    return wrapped_func
