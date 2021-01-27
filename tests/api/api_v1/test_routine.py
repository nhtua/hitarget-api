import pytest
from datetime import datetime
from starlette.status import HTTP_200_OK
from fastapi.encoders import jsonable_encoder

from hitarget.core.config import settings
from hitarget.models.routine import Routine

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.usefixtures("reset_db")
]


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
async def routine_in_db(mongodb, reset_routines, routine_data, user_object_id):
    data = [
        dict(
            end_date=None,
            user_id=user_object_id,
            fixture="yes",
            **routine_data
        ),
        dict(
            end_date=datetime(2021, 6, 30, 0, 0, 0),
            user_id=user_object_id,
            fixture="yes",
            **routine_data
        )
    ]
    result = await mongodb[Routine.__collection__].insert_many(data)
    cursor = mongodb[Routine.__collection__].find({"_id": {"$in": result.inserted_ids}})
    return [x for x in await cursor.to_list(10)]


async def test_create_routine(authorized_client, routine_sample):
    response = await  authorized_client.post(f"{settings.API_V1_PREFIX}/routine",
                                            json=jsonable_encoder(routine_sample))
    assert response.status_code == HTTP_200_OK

    routine = Routine(**response.json())
    assert routine.summary == routine_sample.summary
    assert routine.note == routine_sample.note
    assert routine.duration == routine_sample.duration
    assert routine.end_date == routine_sample.end_date


async def test_list_routine(authorized_client, routine_in_db):
    response = await  authorized_client.get(f"{settings.API_V1_PREFIX}/routine")
    assert response.status_code == HTTP_200_OK

    routines = response.json()
    assert len(routines) == 2
