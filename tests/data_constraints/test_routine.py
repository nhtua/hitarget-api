import pytest
from datetime import datetime, date

from hitarget.models.helper import PyObjectId
from hitarget.models.routine import Checkpoint, FormAddRoutine
from hitarget.business import routine

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.usefixtures(
        "reset_db",
        "checkpoints_data",
        "checkpoints_in_db",
        "routine_data",
        "routine_sample",
        "routine_in_db"
    )
]


async def test_checkpoint_from_dict(checkpoints_data):
    cp = Checkpoint(**checkpoints_data[0])
    assert cp.date == date(2021, 1, 2)


async def test_dict_from_checkpoint(checkpoints_data):
    cp = Checkpoint(**checkpoints_data[0])
    data = cp.dict()
    assert data['date'] == date(2021, 1, 2)


async def test_mongo_date():
    input = date(2021, 2, 10)
    expect = datetime(2021, 2, 10, 23, 59, 59)
    real = routine.mongo_date(input)
    assert real == expect


async def test_mongo_today(patch_today):
    patch_today(2021, 2, 10)
    expect = datetime(2021, 2, 10, 23, 59, 59)
    real = routine.mongo_today()
    assert real == expect


async def test_create_routine(patch_datetime_now, mongodb, user_object_id, routine_data):
    d = [2021, 2, 9, 21, 30, 45]
    patch_datetime_now(*d)
    data = FormAddRoutine(
        summary=routine_data['summary'],
        note=routine_data['note'],
        duration=routine_data['duration'],
        end_date="2021-06-25"
    )
    r = await routine.create_routine(mongodb, data, user_object_id)
    assert isinstance(r.id, PyObjectId)
    assert r.user_id == user_object_id
    assert r.end_date == date(2021, 6, 25)
    assert r.created_at == datetime(*d)
