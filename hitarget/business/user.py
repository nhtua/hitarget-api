from hitarget.core import security
from hitarget.core.errors import EntityDoesNotExist, DuplicatedIdentityKey
from hitarget.core.mongodb import AsyncIOMotorDatabase
from hitarget.models.helper import PyObjectId
from hitarget.models.user import User, UserInDB, FormRegister
from hitarget.resources import strings


async def create_user(db: AsyncIOMotorDatabase, form: FormRegister):
    try:
        existingUser = await find_user_by(db, email=form.email.strip())
    except EntityDoesNotExist:
        existingUser = None

    if existingUser is not None:
        raise DuplicatedIdentityKey(strings.EMAIL_TAKEN)

    user = UserInDB(**form.dict())
    user.salt = security.generate_salt()
    user.password = security.get_password_hash(user.salt + user.password)
    result = await db[user.__collection__].insert_one(user.to_mongo())
    user.id = PyObjectId(str(result.inserted_id))
    return user


async def find_user_by(db: AsyncIOMotorDatabase, id: str = None, email: str = None) -> UserInDB:
    filter = {}
    if id is not None:
        filter["_id"] = PyObjectId(id)
    if email is not None:
        filter["email"] = email.lower()

    result = await db[User.__collection__].find_one(filter)
    if result is None:
        raise EntityDoesNotExist()
    return UserInDB(**result)
