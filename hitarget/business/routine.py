from datetime import datetime, date

from hitarget.core.mongodb import AsyncIOMotorDatabase
from hitarget.models.routine import FormAddRoutine, RoutineInDB, RoutineInResponse
from hitarget.models.helper import PyObjectId, ObjectId


async def add_routine(db: AsyncIOMotorDatabase, form: FormAddRoutine, user_id: ObjectId):
    routine = RoutineInDB(**form.dict())
    routine.created_at = datetime.now()
    routine.user_id = user_id
    result = await db[routine.__collection__].insert_one(routine.dict())
    routine.id = PyObjectId(str(result.inserted_id))
    return routine


async def get_routine_by_user(db: AsyncIOMotorDatabase,
                            user_id: ObjectId = None,
                            email: str = None,
                            is_completed: bool = None):
    filter = {}
    if user_id is not None:
        filter['user_id'] = user_id
    if email is not None:
        filter["email"] = email
    if is_completed is True:
        filter["end_date"] = {"$or": [{
            {"$eq": None},
            {"$lt": date.today()}
        }]}
    cursor = db[RoutineInDB.__collection__].find(filter).sort('created_at', -1)
    result = []
    for doc in await cursor.to_list(100):
        result.append(RoutineInResponse(**doc))
    return result
