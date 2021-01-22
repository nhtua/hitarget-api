import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient

from hitarget.core.config import settings
from hitarget.core.mongodb import AsyncIOMotorDatabase


@pytest.fixture(scope="module")
def app() -> FastAPI:
    from hitarget.main import get_application  # local import for testing purpose

    return get_application()


@pytest.fixture()
async def initialized_app(app: FastAPI) -> FastAPI:
    async with LifespanManager(app):
        yield app


@pytest.fixture
async def mongodb(initialized_app: FastAPI) -> AsyncIOMotorDatabase:
    return initialized_app.state.dbe.get_default_database(settings.MONGODB_NAME)


@pytest.fixture
async def reset_db(initialized_app: FastAPI):
    await initialized_app.state.dbe.drop_database(settings.MONGODB_NAME)


@pytest.fixture
async def client(initialized_app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=initialized_app,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client
