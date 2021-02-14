import math
import copy
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
    return mongo_date(date.today())


def mongo_date(d: date):
    return datetime.combine(d, time(hour=23, minute=59, second=59))


async def create_routine(
    db: AsyncIOMotorDatabase,
    form: FormAddRoutine,
    user_id: ObjectId
) -> RoutineInDB:
    data = form.dict()
    data['user_id'] = user_id
    data['created_at'] = datetime.now()
    routine = RoutineInDB(**data)
    result = await db[routine.__collection__].insert_one(routine.to_mongo())
    routine.id = PyObjectId(str(result.inserted_id))
    return routine


# NOTE: work_in_progress=None by default to get all routines
async def get_routine_by_user(
    db: AsyncIOMotorDatabase,
    user_id: ObjectId,
    is_complete: bool = None
) -> List[RoutineInResponse]:
    filter = {}
    filter['user_id'] = user_id
    if is_complete is False:
        filter["$or"] = [
            {"end_date": {"$eq": None}},
            {"end_date": {"$gt": mongo_today()}}
        ]
    if is_complete is True:
        filter["end_date"] = {
            "$ne": None,
            "$lt": mongo_today()
        }
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
    index = -1
    for i, x in enumerate(routine.repeat):
        assert isinstance(x, Checkpoint)
        if x.date == date.today():
            last = x
            index = i
            break
    else:
        last = Checkpoint(
            date=date.today(),
            percentage = 0,
            gain = 0,
            is_running = cp.is_running,
            last_update = datetime.now()
        )

    last = calculate_gain(last, cp.is_running, routine.duration)
    if index < 0:
        routine.repeat.insert(0, last)
    else:
        routine.repeat[index] = last

    result = await db[RoutineInDB.__collection__].update_one(
        {"_id": routine.id},
        {"$set": {"repeat": routine.to_mongo()['repeat']}}
    )
    if result.matched_count == 0:
        raise EntityDoesNotExist()
    return RoutineInResponse(**routine.dict())


def calculate_gain(
    checkpoint: Checkpoint,
    running_status: bool,
    duration: int
) -> Checkpoint:
    cp = copy.deepcopy(checkpoint)
    current_update = datetime.now()
    if cp.is_running:
        cp.gain += math.floor((current_update - cp.last_update).total_seconds())
        cp.percentage = round(cp.gain / duration * 100, 2)
    cp.is_running = running_status
    cp.last_update = current_update
    return cp
