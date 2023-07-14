import uvicorn

from src.infra.adapters.logging.settings import get_logger_uvicorn
from src.settings import get_settings


def run():
    uvicorn.run(
        'app:app',
        host=get_settings().server_settings.app_default_host,
        port=get_settings().server_settings.app_default_port,
        workers=get_settings().server_settings.workers,
        log_config=get_logger_uvicorn(),
        limit_concurrency=get_settings().server_settings.http_max_connections,
        timeout_graceful_shutdown=get_settings().server_settings.timeout_graceful_shutdown,
    )


if __name__ == '__main__':
    run()
