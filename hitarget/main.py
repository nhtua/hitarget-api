from fastapi import FastAPI

from hitarget.core.config import settings
from hitarget.core import mongodb
from hitarget.api.api_v1.routers import routers

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)


@app.on_event("startup")
async def startup_db_client():
    await mongodb.connect()


@app.on_event("shutdown")
async def shutdown_db_client():
    await mongodb.disconnect()

app.include_router(routers, prefix=settings.API_V1_PREFIX)
