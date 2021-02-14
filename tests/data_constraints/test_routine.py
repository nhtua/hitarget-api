import pytest
from datetime import datetime, date

from hitarget.models.helper import PyObjectId
from hitarget.models.routine import Routine,\
    FormAddRoutine,\
    Checkpoint,\
    CheckpointInRequest
from hitarget.business import routine

pytestmark = [
    pytest.mark.asyncio
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


async def test_get_noncomplete_routine_by_user(patch_today, mongodb, user_object_id, routine_in_db, routine_data):
    patch_today(2021, 2, 9)
    results = await routine.get_routine_by_user(mongodb, user_id=user_object_id, is_complete=False)
    assert len(results) == 2


async def test_get_half_complete_routine_by_user(patch_today, mongodb, user_object_id, routine_in_db, routine_data):
    patch_today(2021, 7, 1)  # this day only 1 routine has end_date=None that exists
    results = await routine.get_routine_by_user(mongodb, user_id=user_object_id, is_complete=False)
    assert len(results) == 1
    assert results[0].duration == 60 * 60 * 2
    assert results[0].user_id == user_object_id
    assert results[0].summary == routine_data['summary']
    assert results[0].note == routine_data['note']
    assert results[0].end_date is None


async def test_get_complete_routine_by_user(patch_today, mongodb, user_object_id, routine_in_db, routine_data):
    patch_today(2021, 7, 1)
    results = await routine.get_routine_by_user(mongodb, user_id=user_object_id, is_complete=True)
    assert len(results) == 1
    assert results[0].duration == 60 * 60 * 2
    assert results[0].user_id == user_object_id
    assert results[0].summary == routine_data['summary']
    assert results[0].note == routine_data['note']
    assert results[0].end_date == date(2021, 6, 30)


async def test_calculate_checkpoint_gain(patch_today, patch_datetime_now):
    patch_today(2021, 2, 9)
    patch_datetime_now(2021, 2, 9, 8, 30, 0)
    before = Checkpoint(
        date = date.today(),
        percentage = 0,
        gain = 0,
        is_running = True,
        last_update = datetime.now()
    )

    patch_datetime_now(2021, 2, 9, 8, 31, 0)
    duration = 60
    after = routine.calculate_gain(before, running_status=True, duration=duration)

    assert after.is_running is True
    assert after.last_update > before.last_update
    assert after.last_update == datetime(2021, 2, 9, 8, 31, 0)
    assert after.date == before.date == date(2021, 2, 9)
    assert after.gain == 60
    assert after.percentage == round(after.gain / duration * 100, 2)


async def test_create_checkpoint_first_time(
    patch_datetime_now,
    patch_today,
    mongodb,
    routine_in_db,
    user_object_id
):
    r = await mongodb[Routine.__collection__].find_one({"end_date": None})
    checkpoint = CheckpointInRequest(routine_id=str(r["_id"]), is_running=True)
    patch_today(2021, 2, 12)
    now = [2021, 2, 12, 8, 30, 0]
    patch_datetime_now(*now)
    result = await routine.update_checkpoint(mongodb, checkpoint, user_object_id)
    assert result.repeat is not None
    cp = result.repeat[0]
    assert cp.date == date.today()
    assert cp.percentage == 0
    assert cp.gain == 0
    assert cp.is_running is True
    assert cp.last_update == datetime(*now)


async def test_create_checkpoint_second_time(
    patch_datetime_now,
    patch_today,
    mongodb,
    routine_in_db,
    user_object_id
):
    patch_today(2021, 2, 12)
    r = await mongodb[Routine.__collection__].find_one({"end_date": None})
    checkpoint = CheckpointInRequest(routine_id=str(r["_id"]), is_running=True)

    now = [2021, 2, 12, 8, 30, 0]
    patch_datetime_now(*now)
    result_1st = await routine.update_checkpoint(mongodb, checkpoint, user_object_id)
    assert result_1st.repeat is not None
    assert result_1st.repeat != []

    now = [2021, 2, 12, 8, 30, 30]
    patch_datetime_now(*now)
    result_2nd = await routine.update_checkpoint(mongodb, checkpoint, user_object_id)
    assert len(result_2nd.repeat) == 1

    cp = result_2nd.repeat[0]
    assert cp.date == date.today()
    assert cp.gain == 30
    assert cp.percentage == round(30 / r['duration'] * 100, 2)
    assert cp.is_running is True
    assert cp.last_update == datetime(*now)
