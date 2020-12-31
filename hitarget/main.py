from fastapi import FastAPI

from hitarget.core.config import settings
from hitarget.api.api_v1.routers import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)
app.include_router(api_router, prefix=settings.API_V1_STR)
