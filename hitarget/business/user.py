from bson import ObjectId

from hitarget.core import security
from hitarget.core.errors import EntityDoesNotExist
from hitarget.core.mongodb import AsyncIOMotorDatabase
from hitarget.models.helper import PyObjectId
from hitarget.models.user import User


async def create_user(db: AsyncIOMotorDatabase, user: User):
    user.salt = security.generate_salt()
    user.password = security.get_password_hash(user.salt + user.password)
    result = await db[user.__collection__].insert_one(user.dict())
    user.id = PyObjectId(str(result.inserted_id))
    return user


async def find_user_by(db: AsyncIOMotorDatabase, id: str = None, email: str = None):
    filter = {}
    # filter["_id"] = None if id is None else ObjectId(id)
    filter["email"] = None if email is None else email

    result = await db[User.__collection__].find_one(filter)
    if result is None:
        raise EntityDoesNotExist()
    return result
