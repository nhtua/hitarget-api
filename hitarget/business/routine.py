from typing import List
from datetime import datetime, date, time

from hitarget.core.mongodb import AsyncIOMotorDatabase
from hitarget.models.routine import FormAddRoutine, RoutineInDB, RoutineInResponse
from hitarget.models.helper import PyObjectId, ObjectId


def mongo_today():
    return datetime.combine(date.today(), time(hour=0, minute=0, second=0))


async def create_routine(db: AsyncIOMotorDatabase, form: FormAddRoutine, user_id: ObjectId):
    data = form.dict()
    data['user_id'] = user_id
    data['created_at'] = datetime.now()
    routine = RoutineInDB(**data)
    result = await db[routine.__collection__].insert_one(routine.to_mongo())
    routine.id = PyObjectId(str(result.inserted_id))
    return routine


# NOTE: work_in_progress=None by default to get all routines
async def get_routine_by_user(db: AsyncIOMotorDatabase,
                            user_id: ObjectId = None,
                            email: str = None,
                            work_in_progress: bool = None) -> List[RoutineInResponse]:
    filter = {}
    if user_id is not None:
        filter['user_id'] = user_id
    if email is not None:
        filter["email"] = email
    if work_in_progress is True:
        filter["end_date"] = {"$or": [{
            {"$eq": None},
            {"$gt": mongo_today()}
        }]}
    if work_in_progress is False:
        filter["end_date"] = {"$and": [{
            {"$ne": None},
            {"$lt": mongo_today()}
        }]}
    cursor = db[RoutineInDB.__collection__].find(filter).sort('created_at', -1)
    result = []
    for doc in await cursor.to_list(100):
        result.append(RoutineInResponse(**doc))
    return result
