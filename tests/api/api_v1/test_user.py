import pytest
from typing import Dict
from bson import ObjectId

from hitarget.core.config import settings
from hitarget.models.user import User, FormLogin

pytestmark = pytest.mark.asyncio


async def test_create_user(user_data, client, mongodb):
    response = await client.post(f"{settings.API_V1_PREFIX}/users/register", json=user_data)
    r_user = response.json()
    col = mongodb[User.__collection__]
    u = await col.find_one({"_id": ObjectId(r_user["id"])})

    assert response.status_code == 201
    assert 'password' not in r_user
    assert 'id' in r_user
    assert u is not None
    assert r_user['email'] == user_data['email'] == u['email']
    assert r_user['name']  == user_data['name']


async def test_user_in_db(user_data, mongodb):
    # BE CAREFUL with the test order.
    # Database won't be clear until `reset_db` been invoked
    col = mongodb[User.__collection__]
    u = await col.find_one({"email": user_data["email"]})
    assert u is not None


async def test_reset_db(mongodb, reset_db):
    collection = mongodb[User.__collection__]
    u = await collection.find_one({"email": "someone@email.com"})
    assert u is None


async def test_login(client, user_data, user_in_db):
    form = FormLogin(**user_data)
    response = await client.post(f"{settings.API_V1_PREFIX}/users/login", json=form.dict())
    assert response.status_code == 200
    response = response.json()
    assert response['email'] == user_in_db.email
    assert response['name']  == user_in_db.name
    assert response['token'] != ""
