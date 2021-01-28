import pytest
import jwt
from datetime import timedelta

from hitarget.services.jwt import \
    create_jwt_token,\
    create_access_token_for_user,\
    get_email_from_token,\
    get_user_id_from_token
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


async def test_create_access_token_for_user(test_user):
    real_token = create_access_token_for_user(test_user)
    decode = jwt.decode(real_token, key=settings.JWT_SECRET, verify=True, algorithms=[settings.JWT_ALGORITHM])

    assert decode['email'] == test_user.email
    assert decode['name']  == test_user.name


async def test_get_email_from_token(test_user):
    real_token = create_access_token_for_user(test_user)
    email = get_email_from_token(real_token)

    assert email == test_user.email


async def test_get_user_id_from_token(test_user):
    real_token = create_access_token_for_user(test_user)
    user_id = get_user_id_from_token(real_token)

    assert user_id == test_user.id


def test_error_when_wrong_token() -> None:
    with pytest.raises(ValueError):
        get_email_from_token("asdf")
