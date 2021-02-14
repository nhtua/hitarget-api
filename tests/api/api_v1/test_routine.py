import pytest

from starlette.status import HTTP_200_OK
from fastapi.encoders import jsonable_encoder

from hitarget.core.config import settings
from hitarget.models.routine import Routine

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.usefixtures("reset_db", "routine_data", "routine_sample", "routine_in_db")
]


async def test_create_routine(authorized_client, reset_routines, routine_sample):
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
