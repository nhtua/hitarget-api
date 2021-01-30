from fastapi import APIRouter
from .endpoints import health
from .endpoints import authentication
from .endpoints import routine
from .endpoints import user

routers = APIRouter()
routers.include_router(health.router)
routers.include_router(authentication.router)
routers.include_router(routine.router)
routers.include_router(user.router)
