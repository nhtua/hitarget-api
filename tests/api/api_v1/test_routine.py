import pytest
from datetime import date
from starlette.status import HTTP_200_OK
from fastapi.encoders import jsonable_encoder

from hitarget.core.config import settings
from hitarget.models.routine import Routine

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.usefixtures("reset_db")
]


@pytest.fixture(params=[None, date(2021, 6, 30)])
def routine_sample(request) -> Routine:
    return Routine(
        summary ="Slowly build hitarget",
        note    ="keep it grown daily",
        duration=60 * 60 * 2,  # 2 hours
        end_date=request.param
    )


async def test_create_routine(authorized_client, routine_sample):
    response = await  authorized_client.post(f"{settings.API_V1_PREFIX}/routine",
                                            json=jsonable_encoder(routine_sample))
    assert response.status_code == HTTP_200_OK

    routine = Routine(**response.json())
    assert routine.summary == routine_sample.summary
    assert routine.note == routine_sample.note
    assert routine.duration == routine_sample.duration
    assert routine.end_date == routine_sample.end_date
