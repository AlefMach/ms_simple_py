import logging.config
from copy import deepcopy
from typing import Any, Dict

from uvicorn.config import LOGGING_CONFIG as UVICORN_LOGGING_CONFIG

from src.settings import get_settings

logger = logging.getLogger(__name__)


class EndpointFilter(logging.Filter):
    """
    Uvicorn endpoint access log filter
    """

    def filter(self, record: logging.LogRecord) -> bool:
        return (
            record.getMessage().find('GET /metrics') == -1 and record.getMessage().find('GET /healthcheck') == -1
        )


# https://docs.python.org/3/library/logging.config.html#dictionary-schema-details
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': get_settings().log_settings.log_format,
            'datefmt': get_settings().log_settings.date_format,
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': get_settings().log_settings.log_level,
            'formatter': 'standard',
            'stream': 'ext://sys.stdout',
        },
    },
    'root': {
        'level': get_settings().log_settings.log_level,
        'handlers': [
            'console',
        ],
    },
    'loggers': {
        'src': {
            'level': get_settings().log_settings.log_level,
            'qualname': 'src',
        },
        'grpc': {
            'level': get_settings().log_settings.log_level,
            'qualname': 'grpc',
        },
        'urllib3': {
            'level': get_settings().log_settings.log_level,
            'qualname': 'urllib3',
        },
        'sqlalchemy': {
            'level': get_settings().log_settings.log_level_sqlalchemy,
            'qualname': 'sqlalchemy',
            'formatter': ['standard'],
        },
        'sqlalchemy.engine': {
            'level': get_settings().log_settings.log_level_sqlalchemy,
            'qualname': 'sqlalchemy.engine',
            'formatter': ['standard'],
        },
        'sqlalchemy.pool': {
            'level': get_settings().log_settings.log_level_sqlalchemy,
            'qualname': 'sqlalchemy.pool',
            'formatter': ['standard'],
        },
        'asyncpg.pool': {
            'level': get_settings().log_settings.log_level_sqlalchemy,
            'qualname': 'asyncpg.pool',
            'formatter': ['standard'],
        },
        'asyncio': {
            'level': get_settings().log_settings.log_level,
            'qualname': 'asyncio',
        },
        'fastapi': {
            'level': get_settings().log_settings.log_level,
            'qualname': 'fastapi',
        },
    },
}


def get_logger_uvicorn() -> Dict[str, Any]:
    FORMATTERS = 'formatters'
    DEFAULT = 'default'
    ACCESS = 'access'
    FMT = 'fmt'
    DATEFMT = 'datefmt'
    FILTERS = 'filters'
    SKIP_ENDPOINT = 'skip_endpoint'
    HANDLERS = 'handlers'
    # https://github.com/tiangolo/fastapi/discussions/7457#discussioncomment-5565969
    uvicorn_log_config = deepcopy(UVICORN_LOGGING_CONFIG)
    uvicorn_log_config[FORMATTERS][DEFAULT][FMT] = get_settings().log_settings.log_format
    uvicorn_log_config[FORMATTERS][ACCESS][FMT] = get_settings().log_settings.log_format_access
    uvicorn_log_config[FORMATTERS][ACCESS][DATEFMT] = get_settings().log_settings.date_format
    uvicorn_log_config[FORMATTERS][DEFAULT][DATEFMT] = get_settings().log_settings.date_format
    uvicorn_log_config[FILTERS] = {
        SKIP_ENDPOINT: {
            '()': 'src.infra.adapters.logging.settings.EndpointFilter',
        }
    }
    uvicorn_log_config[HANDLERS][ACCESS][FILTERS] = [SKIP_ENDPOINT]
    return uvicorn_log_config


def set_up_logger():
    logging.config.dictConfig(LOGGING_CONFIG)


def debug_logger():
    for key, value in logging.root.manager.loggerDict.items():
        if not isinstance(value, logging.PlaceHolder):
            formatter = None
            if value.handlers and value.handlers[0].formatter:
                formatter = value.handlers[0].formatter.__dict__['_fmt']
            if value.parent.handlers and value.parent.handlers[0].formatter:
                formatter = value.parent.handlers[0].formatter.__dict__['_fmt']

            config_log = f'{key, logging.getLevelName(value.level) if hasattr(value, "level") else None, value.handlers, value.filters, value.parent.name, formatter}'  # noqa E501
            logger.info(config_log)
