import pytest
from datetime import datetime

from hitarget.models.routine import Routine, RoutineInDB, Checkpoint


@pytest.fixture
def routine_data():
    return {
        "summary" : "Slowly build hitarget",
        "note"    : "keep it grown daily",
        "duration": 60 * 60 * 2,  # 2 hours
    }


@pytest.fixture(params=[None, datetime(2021, 6, 30, 0, 0, 0)])
def routine_sample(request, routine_data) -> Routine:
    return Routine(
        end_date=request.param,
        **routine_data
    )


@pytest.fixture
async def routine_in_db(
    mongodb,
    reset_routines,
    routine_data,
    user_object_id
) -> RoutineInDB:
    data = [
        dict(
            end_date=None,
            user_id=user_object_id,
            created_at=datetime(2021, 2, 1, 8, 30, 0),
            fixture="yes",
            **routine_data
        ),
        dict(
            end_date=datetime(2021, 6, 30, 23, 59, 59),
            user_id=user_object_id,
            created_at=datetime(2021, 2, 1, 8, 30, 0),
            fixture="yes",
            **routine_data
        )
    ]
    result = await mongodb[Routine.__collection__].insert_many(data)
    cursor = mongodb[Routine.__collection__].find({"_id": {"$in": result.inserted_ids}})
    return [RoutineInDB(**x) for x in await cursor.to_list(2)]


@pytest.fixture
def checkpoints_data():
    return [
        dict(
            date='2021-01-02',
            percentage=80.5,
            gain=2898,
            is_running=True,
            last_update=datetime(2021, 1, 2, 9, 15, 30)
        ),
        dict(
            date='2021-01-01',
            percentage=90,
            gain=3240,
            is_running=True,
            last_update=datetime(2021, 1, 2, 9, 20, 30)
        )
    ]


@pytest.fixture
def checkpoints_in_db(checkpoints_data):
    data = []
    for x in checkpoints_data:
        data += [Checkpoint(**x)]
    return data
