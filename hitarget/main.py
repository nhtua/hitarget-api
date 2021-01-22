from fastapi import FastAPI

from hitarget.core.config import settings
from hitarget.core import mongodb
from hitarget.api.api_v1.routers import routers


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
    )

    @application.on_event("startup")
    async def startup_db_client():
        application.state.dbe = await mongodb.connect()

    @application.on_event("shutdown")
    async def shutdown_db_client():
        await mongodb.disconnect()

    application.include_router(routers, prefix=settings.API_V1_PREFIX)
    return application


app = get_application()
