from fastapi import FastAPI

from settings import Settings
from web.http.v1.root import v1_router


def create_application(settings: Settings) -> FastAPI:
    application = FastAPI(
        title=settings.DOCS_TITLE,
        description=settings.DOCS_DESCRIPTION,
        openapi_url=settings.OPENAPI_URL,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOCS_URL
    )

    register_routers(application=application)
    return application


def register_routers(application: FastAPI) -> None:
    """Register the routers"""

    application.include_router(v1_router)
