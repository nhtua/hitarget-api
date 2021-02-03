import math
from typing import List
from datetime import datetime, date, time

from hitarget.core.mongodb import AsyncIOMotorDatabase
from hitarget.models.routine import FormAddRoutine,\
    RoutineInDB,\
    RoutineInResponse,\
    CheckpointInRequest,\
    Checkpoint
from hitarget.models.helper import PyObjectId, ObjectId
from hitarget.core.errors import EntityDoesNotExist


def mongo_today():
    return datetime.combine(date.today(), time(hour=0, minute=0, second=0))


async def create_routine(
    db: AsyncIOMotorDatabase,
    form: FormAddRoutine,
    user_id: ObjectId
):
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
        id = doc.pop('_id')
        result += [RoutineInResponse(id=id, **doc)]
    return result


async def update_checkpoint(
    db: AsyncIOMotorDatabase,
    cp: CheckpointInRequest,
    user_id: ObjectId
) -> RoutineInResponse:
    routine = await db[RoutineInDB.__collection__].find_one({
        "_id": ObjectId(cp.routine_id),
        "user_id": user_id
    })
    if routine is None:
        raise EntityDoesNotExist()

    routine = RoutineInDB(**routine)
    last = None
    for i, x in enumerate(routine.repeat):
        if x.date == date.today():
            last = routine.repeat.pop(i)
            break
    else:
        last = Checkpoint(
            date=date.today(),
            percentage = 0,
            gain = 0,
            is_running = cp.is_running,
            last_update = datetime.now()
        )
    current_update = datetime.now()
    if last.is_running:
        last.gain += math.floor((current_update - last.last_update).total_seconds())
        last.percentage = round(last.gain / routine.duration * 100, 2)
    last.is_running = cp.is_running
    last.last_update = current_update

    routine.repeat.insert(0, last)
    result = await db[RoutineInDB.__collection__].update_one(
        {"_id": routine.id},
        {"$set": {"repeat": routine.to_mongo()['repeat']}}
    )
    if result.matched_count == 0:
        raise EntityDoesNotExist()
    return RoutineInResponse(**routine.dict())
