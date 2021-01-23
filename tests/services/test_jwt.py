import pytest
import jwt
from datetime import timedelta

from hitarget.services.jwt import create_jwt_token, create_access_token_for_user, get_email_from_token
from hitarget.core.config import settings

pytestmark = pytest.mark.asyncio


async def test_create_jwt_token():
    payload = {"content": "payload"}
    real_token = create_jwt_token(
        jwt_content=payload,
        secret_key="secret",
        expires_delta=timedelta(minutes=1))
    decode = jwt.decode(real_token, key="secret", verify=True, algorithms=[settings.JWT_ALGORITHM])

    assert decode['content'] == 'payload'


async def test_create_access_token_for_user(user_in_response):
    real_token = create_access_token_for_user(user_in_response)
    decode = jwt.decode(real_token, key=settings.JWT_SECRET, verify=True, algorithms=[settings.JWT_ALGORITHM])

    assert decode['email'] == user_in_response.email
    assert decode['name']  == user_in_response.name


async def test_get_email_from_token(user_in_response):
    real_token = create_access_token_for_user(user_in_response)
    email = get_email_from_token(real_token)

    assert email == user_in_response.email
