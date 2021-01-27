import pytest
from starlette.status import HTTP_200_OK
from fastapi.encoders import jsonable_encoder

from hitarget.core.config import settings
from hitarget.models.routine import Routine

pytestmark = pytest.mark.asyncio


async def test_create_routine(reset_users, reset_routines,
                              user_in_db, authorized_client, routine_sample):
    response = await  authorized_client.post(f"{settings.API_V1_PREFIX}/routine",
                                            json=jsonable_encoder(routine_sample))
    assert response.status_code == HTTP_200_OK

    routine = Routine(**response.json())
    assert routine.summary == routine_sample.summary
    assert routine.note == routine_sample.note
    assert routine.duration == routine_sample.duration
    assert routine.end_date == routine_sample.end_date
