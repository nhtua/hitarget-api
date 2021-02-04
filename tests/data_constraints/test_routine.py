import pytest
from datetime import datetime, date

from hitarget.models.routine import Checkpoint

pytestmark = pytest.mark.asyncio


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


async def test_checkpoint_from_dict(checkpoints_data):
    cp = Checkpoint(**checkpoints_data[0])
    assert cp.date == date(2021, 1, 2)


async def test_dict_from_checkpoint(checkpoints_data):
    cp = Checkpoint(**checkpoints_data[0])
    data = cp.dict()
    assert data['date'] == date(2021, 1, 2)
