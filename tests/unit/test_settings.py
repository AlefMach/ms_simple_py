import os
from unittest import mock

import src.settings


def test_otlp_settings_with_mock_enviroments_values(os_enviroments_otlp_mock):
    # arrange
    with mock.patch.dict(os.environ, os_enviroments_otlp_mock):
        # act
        otlp_settings = src.settings.OTLPSettings()

    # assert
    assert otlp_settings.otlp_agent_host == '0.0.0.0'
    assert otlp_settings.otlp_agent_grpc_port == 1111
    assert otlp_settings.otlp_agent_http_port == 2222
    assert otlp_settings.otlp_agent_auth_token == 'test_token'


def test_log_settings_with_mock_enviroments_values(os_enviroments_log_mock):
    # arrange
    with mock.patch.dict(os.environ, os_enviroments_log_mock):
        # act
        log_settings = src.settings.LogSettings()

    # assert
    assert log_settings.log_level == 'INFO'
    assert log_settings.log_format == '{level} | {message}'


def test_server_settings_with_mock_enviroments_values(os_enviroments_server_mock):
    # arrange
    with mock.patch.dict(os.environ, os_enviroments_server_mock):
        # act
        server_settings = src.settings.ServerSettings()

    # assert
    assert isinstance(server_settings.project_contact_api, dict)
    assert isinstance(server_settings.project_name_api, str)
    assert isinstance(server_settings.project_version_api, str)
    assert server_settings.app_default_host == 'test_host'
    assert server_settings.app_default_port == 8888
    assert server_settings.environment == 'test'
    assert server_settings.http_max_connections == 1
    assert server_settings.workers == 2


def test_database_settings_with_mock_enviroments_values(os_enviroments_database_mock):
    # arrange
    with mock.patch.dict(os.environ, os_enviroments_database_mock):
        # act
        database_settings = src.settings.DatabaseSettings()

    # assert
    assert database_settings.database_port == 5432
    assert database_settings.database_host == 'test_host'
    assert database_settings.database_user == 'test_database_user'
    assert database_settings.database_password == 'test_database_password'
    assert database_settings.database_pool_size == 99
    assert database_settings.database_pool_timeout_seconds == 99
    assert database_settings.database_max_overflow == 99
    assert database_settings.database_pool_recicle_seconds == 99
    assert database_settings.database_echo_sql == 'debug'
    assert database_settings.database_page_size == 1


def test_database_async_uri(os_enviroments_database_mock):
    # arrange
    with mock.patch.dict(os.environ, os_enviroments_database_mock):
        # act
        database_settings = src.settings.DatabaseSettings()

    # assert
    assert (
        database_settings.database_async_uri
        == 'postgresql+asyncpg://test_database_user:test_database_password@test_host:5432/test_database_name'
    )
