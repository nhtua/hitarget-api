from fastapi import FastAPI

from hitarget.core.config import settings
from hitarget.api.api_v1.routers import routers

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)
app.include_router(routers, prefix=settings.API_V1_PREFIX)
