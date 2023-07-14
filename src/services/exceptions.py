import logging
from typing import Any, Optional

from fastapi import HTTPException
from starlette import status

logger = logging.getLogger(__name__)


class APIException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: str = 'Operation error',
        log_level: Optional[int] = logging.INFO,
        stacktrace=None,
    ):
        self.status_code = status_code
        self.detail = detail
        log_detail = f'[-] {detail} - Status=[{status_code}]'

        if stacktrace:
            log_detail += f' Stacktrace=[{stacktrace}]'
        match log_level:
            case logging.INFO:
                logger.info(log_detail)
            case logging.WARNING:
                logger.warning(log_detail)
            case logging.CRITICAL:
                logger.critical(log_detail)
            case logging.DEBUG:
                logger.debug(log_detail)
            case logging.ERROR:
                logger.error(log_detail)

        super().__init__(status_code, detail)


class UniqueException(APIException):
    def __init__(self, stacktrace: list):
        detail = 'Unique constraint - the value already exists in the database'
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            stacktrace=stacktrace,
            log_level=logging.WARNING,
        )


class UnprocessableException(APIException):
    def __int__(self, stacktrace: list, detail='Item requisitado não é válido '):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            stacktrace=stacktrace,
            log_level=logging.WARNING,
        )


class ValidationException(APIException):
    def __init__(self, stacktrace: list):
        detail = 'Validation error - some value of the response model is not a valid type'
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail, stacktrace=stacktrace)


class SQLAlchemyException(APIException):
    def __init__(self, stacktrace: list):
        detail = 'SQLAlchemy - error detected in the ORM or database'
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            stacktrace=stacktrace,
            log_level=logging.CRITICAL,
        )


class AuthenticationException(APIException):
    def __init__(self, stacktrace: list):
        detail = 'Authentication - error detected in the Authentication process'
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail=detail, stacktrace=stacktrace, log_level=logging.CRITICAL
        )


class UnauthorizedException(APIException):
    def __init__(self, stacktrace: list, kid: Optional[Any] = ''):
        detail = 'Unauthorized - Invalid or expired token'

        if kid:
            detail += f' - Kid=[{kid}]'

        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            stacktrace=stacktrace,
            log_level=logging.WARNING,
        )


class NotFoundException(APIException):
    def __init__(self, model: str = 'Values'):
        detail = f'{model} not found'
        super().__init__(status_code=status.HTTP_204_NO_CONTENT, detail=detail)


class InvalidDocumentException(APIException):
    def __init__(self):
        detail = 'Invalid CPF/CNPJ'
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)
