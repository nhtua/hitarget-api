import pytest


from hitarget.core.config import settings
from hitarget.core.mongodb import AsyncIOMotorDatabase
from hitarget.models.user import User
from hitarget.tests.conftest import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_create_user(client: AsyncClient):
    user_data = dict(
        email="someone@email.com",
        password="password",
    )
    response = await client.post(f"{settings.API_V1_PREFIX}/users", json=user_data)
    r_user = response.json()

    assert response.status_code == 201
    assert 'password' not in r_user
    assert 'id' in r_user
    assert r_user['email'] == user_data['email']
    assert r_user['name'] is None


async def test_reset_db(mongodb: AsyncIOMotorDatabase, reset_db: None):
    collection = mongodb[User.__collection__]
    u = await collection.find_one({"email": "someone@email.com"})
    assert u is None
