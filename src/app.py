from fastapi import FastAPI

from src.entrypoints import router
from src.infra.adapters.logging.settings import set_up_logger
from src.settings import get_settings


def create_app():
    _app = FastAPI(
        title=get_settings().server_settings.project_description_api,
        version=get_settings().server_settings.project_version_api,
        contact=get_settings().server_settings.project_contact_api,
        on_startup=[set_up_logger],
    )
    _app.include_router(router)

    return _app


app = create_app()


@app.on_event('startup')
async def startup_event():
    """On startup"""
