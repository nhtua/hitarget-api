import pytest
import asyncio
import copy
from typing import Dict
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from bson import ObjectId

from hitarget.core.config import settings
from hitarget.core.mongodb import AsyncIOMotorDatabase
from hitarget.core import security
from hitarget.models.user import UserInDB, UserInResponse
from hitarget.models.routine import Routine
from hitarget.services.jwt import create_access_token_for_user

from tests.fixtures.routine import *


# This workaround works
# for https://github.com/pytest-dev/pytest-asyncio/issues/38#issuecomment-264418154
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
def app() -> FastAPI:
    from hitarget.main import get_application  # local import for testing purpose

    return get_application()


@pytest.fixture(scope="module")
async def initialized_app(app: FastAPI) -> FastAPI:
    async with LifespanManager(app):
        yield app


@pytest.fixture(scope="module")
async def mongodb(initialized_app: FastAPI) -> AsyncIOMotorDatabase:
    return initialized_app.state.dbe.get_default_database(settings.MONGODB_NAME)


@pytest.fixture(scope="module")
async def reset_db(initialized_app: FastAPI):
    await initialized_app.state.dbe.drop_database(settings.MONGODB_NAME)


@pytest.fixture
async def reset_users(mongodb: AsyncIOMotorDatabase):
    await mongodb[UserInDB.__collection__].drop()


@pytest.fixture
async def reset_routines(mongodb: AsyncIOMotorDatabase):
    await mongodb[Routine.__collection__].drop()


@pytest.fixture
async def client(initialized_app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=initialized_app,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture
def user_data() -> Dict:
    return dict(
        email="someone@email.com",
        password="password",
        name='Ariel Bega'
    )


@pytest.fixture
def user_object_id() -> ObjectId:
    return ObjectId('600ba0839e62bfc697974862')


@pytest.fixture
async def user_in_db(reset_users, user_data: Dict, user_object_id: ObjectId, mongodb: AsyncIOMotorDatabase) -> UserInDB:
    data = user_data.copy()
    data['_id'] = user_object_id
    data['salt'] = security.generate_salt()
    data['password'] = security.get_password_hash(data['salt'] + data['password'])
    result = await mongodb.users.insert_one(data)
    result = await  mongodb.users.find_one({"_id": result.inserted_id})
    return UserInDB(**result)


@pytest.fixture
def test_user(user_data: Dict, user_object_id: ObjectId) -> UserInResponse:
    u = UserInResponse(**user_data)
    u.id = user_object_id
    return u


@pytest.fixture
def token(user_in_db: UserInDB) -> str:
    test_user = UserInResponse(**user_in_db.dict())
    return create_access_token_for_user(test_user)


@pytest.fixture
def authorization_prefix() -> str:
    from hitarget.core.config import settings
    return settings.JWT_TOKEN_PREFIX


@pytest.fixture
def authorized_client(
    client: AsyncClient,
    token: str,
    authorization_prefix: str
) -> AsyncClient:
    client.headers = {
        "Authorization": f"{authorization_prefix} {token}",
        **client.headers,
    }
    return client


@pytest.fixture
def patch_datetime_now(monkeypatch):
    def wrapper(*args, **kwargs):
        import datetime
        fake_datetime = datetime.datetime(*args, **kwargs)

        def mock_now():
            return copy.deepcopy(fake_datetime)

        monkeypatch.setattr(datetime.datetime, 'now', mock_now)
        monkeypatch.setattr(datetime.datetime, 'today', mock_now)
    return wrapper


@pytest.fixture
def patch_today(monkeypatch):
    def wrapper(*args, **kwargs):
        import datetime
        fake_date = datetime.date(*args, **kwargs)

        def mock_today():
            return fake_date

        monkeypatch.setattr(datetime.date, 'today', mock_today)
    return wrapper
