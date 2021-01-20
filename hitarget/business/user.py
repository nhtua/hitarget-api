from hitarget.core import security
from hitarget.core.mongodb import AsyncIOMotorDatabase
from hitarget.models.helper import PyObjectId
from hitarget.models.user import User


async def create_user(db: AsyncIOMotorDatabase, user: User):
    user.salt = security.generate_salt()
    user.password = security.get_password_hash(user.salt + user.password)
    result = await db[user.__collection__].insert_one(user.dict())
    user.id = PyObjectId(str(result.inserted_id))
    return user
