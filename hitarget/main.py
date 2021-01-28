from fastapi import FastAPI
from starlette.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError

from hitarget.core.config import settings
from hitarget.api.errors.http_error import http_error_handler
from hitarget.api.errors.validation_error import http422_error_handler
from hitarget.api.api_v1.routers import routers
from hitarget.core.events import create_start_app_handler, create_stop_app_handler


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
    )

    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(routers, prefix=settings.API_V1_PREFIX)
    return application


app = get_application()
