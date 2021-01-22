import pytest
from typing import Dict
from bson import ObjectId

from hitarget.core.config import settings
from hitarget.core.mongodb import AsyncIOMotorDatabase
from hitarget.models.user import User
from hitarget.tests.conftest import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_create_user(user_data: Dict, client: AsyncClient, mongodb: AsyncIOMotorDatabase):
    response = await client.post(f"{settings.API_V1_PREFIX}/users/register", json=user_data)
    r_user = response.json()
    col = mongodb[User.__collection__]
    u = await col.find_one({"_id": ObjectId(r_user["id"])})

    assert response.status_code == 201
    assert 'password' not in r_user
    assert 'id' in r_user
    assert u is not None
    assert r_user['email'] == user_data['email'] == u['email']
    assert r_user['name'] is None


async def test_user_in_db(user_data: Dict, mongodb: AsyncIOMotorDatabase):
    # BE CAREFUL with the test order.
    # Database won't be clear until `reset_db` been invoked
    col = mongodb[User.__collection__]
    u = await col.find_one({"email": user_data["email"]})
    assert u is not None


async def test_reset_db(mongodb: AsyncIOMotorDatabase, reset_db: None):
    collection = mongodb[User.__collection__]
    u = await collection.find_one({"email": "someone@email.com"})
    assert u is None
