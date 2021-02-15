import pytest

from hitarget.models.user import FormRegister
from hitarget.business.user import create_user
from hitarget.core.errors import DuplicatedIdentityKey


pytestmark = pytest.mark.asyncio


async def test_create_new_user(mongodb, reset_users, user_data):
    form = FormRegister(**user_data)
    user = await create_user(mongodb, form)
    assert user.id is not None
    assert user.email == user_data['email']
    assert user.name == user_data['name']


async def test_create_user_by_existing_email(mongodb, user_in_db, user_data):
    form = FormRegister(**user_data)
    with pytest.raises(DuplicatedIdentityKey):
        await create_user(mongodb, form)
