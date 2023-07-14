import os
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Optional

import tomli
from pydantic import BaseSettings, Field


class Env(str, Enum):
    HML = 'hml'
    STAGING = 'staging'
    PRD = 'prd'
    UNITTEST = 'unittest'
    LOCAL = 'local'


def is_env(env: Env):
    return get_settings().server_settings.environment == env.value


class OtlpExporterProtocol(str, Enum):
    GRPC = 'grpc'
    HTTP = 'http'


def is_otlp_exporter_protocol(otlp_exporter_protocol: OtlpExporterProtocol):
    return get_settings().otlp_settings.otlp_exporter_protocol == otlp_exporter_protocol.value


class ServerSettings(BaseSettings):
    app_default_host: str = Field('0.0.0.0', env='APP_DEFAULT_HOST')
    app_default_port: int = Field(8000, env='APP_DEFAULT_PORT')
    http_max_connections: int = Field(2000, env='HTTP_MAX_CONNECTIONS')
    workers: int = Field(1, env='WORKERS')
    environment: str = Field(..., env='ENVIRONMENT')
    timeout_graceful_shutdown: int = Field(5, env='TIMEOUT_GRACEFUL_SHUTDOWN')
    deployment_name: str = Field(None, env='DEPLOYMENT_NAME')

    @property
    def project_name_api(self):
        return self._get_poetry().get('name').replace('.', '-')

    @property
    def project_version_api(self):
        return self._get_poetry().get('version')

    @property
    def project_description_api(self):
        return self._get_poetry().get('description')

    @property
    def project_contact_api(self):
        return {'contatos': self._get_contact()}

    def _get_poetry(self):
        with open(f'{Path(__file__).resolve().parent.parent}{os.sep}pyproject.toml', 'rb') as reader:
            pyproject = tomli.load(reader)
        return pyproject['tool']['poetry']

    def _get_contact(self):
        with open(f'{Path(__file__).resolve().parent.parent}{os.sep}pyproject.toml', 'rb') as reader:
            pyproject = tomli.load(reader)
        return pyproject['information']['contact']


class DatabaseSettings(BaseSettings):
    database_pool_size: int = Field(20, env='DATABASE_POOL_SIZE')
    database_pool_timeout_seconds: int = Field(5, env='DATABASE_POOL_TIMEOUT_SECONDS')
    database_max_overflow: int = Field(10, env='DATABASE_MAX_OVERFLOW')
    database_pool_recicle_seconds: int = Field(3600, env='DATABASE_POOL_RECICLE_SECONDS')
    database_echo_sql_option: str = Field(None, env='DATABASE_ECHO_SQL')
    database_port: int = Field(5432, env='DATABASE_PORT')
    database_host: str = Field('localhost', env='DATABASE_HOST')
    database_name: str = Field(..., env='DATABASE_NAME')
    database_user: str = Field(..., env='DATABASE_USER')
    database_password: str = Field(..., env='DATABASE_PASSWORD')
    database_page_size: int = Field(1000, env='PAGE_SIZE')

    @property
    def database_echo_sql(self):
        """
        see: https://github.com/sqlalchemy/sqlalchemy/blob/8d16aac95d99c708ff4eecc9f8676776c27cfd58/lib/sqlalchemy/log.py#L128
        """
        return (
            self.database_echo_sql_option
            if self.database_echo_sql_option == 'debug'
            else bool(self.database_echo_sql_option)
        )

    @property
    def database_async_uri(self):
        return self._get_database_uri(driver='asyncpg')

    def _get_database_uri(self, driver: str = 'asyncpg') -> str:
        return f'postgresql+{driver}://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}'  # noqa E501

    @property
    def database_unittest_async_uri(self):
        return f'sqlite+aiosqlite:///{Path(__file__).resolve().parent.parent}{os.sep}unit_test.db'

    @property
    def database_unittest_sync_uri(self):
        return f'sqlite:///{Path(__file__).resolve().parent.parent}{os.sep}unit_test.db'


class OTLPSettings(BaseSettings):
    datadog_host: Optional[str] = Field(None, env='DATADOG_HOST')
    tempo_host: Optional[str] = Field(None, env='TEMPO_HOST')
    otlp_agent_grpc_port: Optional[int] = Field(4317, env='OTLP_AGENT_GRPC_PORT')
    otlp_agent_http_port: Optional[int] = Field(4318, env='OTLP_AGENT_HTTP_PORT')
    otlp_agent_auth_token: Optional[str] = Field(None, env='OTLP_AGENT_AUTH_TOKEN')
    otlp_exporter_protocol: Optional[str] = Field('http', env='OTLP_EXPORTER_PROTOCOL')
    otlp_sqlalchemy_enable_commenter: bool = Field(False, env='OTLP_SQLALCHEMY_ENABLE_COMMENTER')

    @property
    def otlp_agent_host(self):
        if is_env(Env.PRD):
            return self.datadog_host
        if is_env(Env.STAGING):
            return self.datadog_host
        return self.tempo_host


class LogSettings(BaseSettings):
    log_level: str = Field('ERROR', env='LOG_LEVEL')
    log_format: str = Field(
        '%(asctime)s %(levelname)s %(process)d [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s] [%(name)s] [%(filename)s:%(lineno)d] - %(message)s',  # noqa E501
        env='LOG_FORMAT',
    )
    log_format_access: str = Field(
        '%(asctime)s %(levelname)s %(process)d [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s] %(client_addr)s - "%(request_line)s" %(status_code)s',  # noqa E501
        env='LOG_FORMAT_ACCESS',
    )
    date_format: str = Field('%Y-%m-%d %H:%M:%S', env='DATE_FORMAT')
    log_level_sqlalchemy: str = Field('ERROR', env='LOG_LEVEL_SQLALCHEMY')


class BrokerSettings(BaseSettings):
    any_api_external: str = Field('http://localhost:xpto', env='ANY_API_MAYBE_A_ACL')

class FutureData(BaseSettings):
    months: int = Field(1, env='INSTALLMENTS_MONTHS')
    days: int = Field(0, env='INSTALLMENTS_DAYS')


class EnvSettings(BaseSettings):
    broker_settings = BrokerSettings()
    log_settings = LogSettings()
    database_settings = DatabaseSettings()
    otlp_settings = OTLPSettings()
    server_settings = ServerSettings()
    future_data = FutureData()


@lru_cache
def get_settings() -> EnvSettings:
    return EnvSettings()
