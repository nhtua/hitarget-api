import pytest
from typing import Dict
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from bson import ObjectId

from hitarget.core.config import settings
from hitarget.core.mongodb import AsyncIOMotorDatabase
from hitarget.core import security
from hitarget.models.user import UserInDB, UserInResponse


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


@pytest.fixture
async def user_data() -> Dict:
    return dict(
        email="someone@email.com",
        password="password",
        name='Ariel Bega'
    )


@pytest.fixture
async def user_in_db(user_data: Dict, mongodb: AsyncIOMotorDatabase) -> UserInDB:
    user_data['salt'] = security.generate_salt()
    user_data['password'] = security.get_password_hash(user_data['salt'] + user_data['password'])
    result = await mongodb.users.insert_one(user_data)
    result = await  mongodb.users.find_one({"_id": result.inserted_id})
    return UserInDB(**result)


@pytest.fixture
async def user_in_response(user_data: Dict) -> UserInResponse:
    u = UserInResponse(
        id=ObjectId('600ba0839e62bfc697974862'),
        email=user_data['email'],
        name=user_data['name'],
        token=None
    )
    return u
