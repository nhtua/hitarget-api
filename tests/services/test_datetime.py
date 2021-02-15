import pytest
from datetime import datetime, date

pytestmark = pytest.mark.asyncio


async def test_mock_today(patch_today):
    patch_today(2021, 2, 9)
    expect = date(2021, 2, 9)
    assert date.today() == expect

    patch_today(2021, 2, 10)
    expect = date(2021, 2, 10)
    assert date.today() == expect


async def test_mock_now(patch_datetime_now):
    patch_datetime_now(2021, 2, 8, 23, 59, 59)
    expect = datetime(2021, 2, 8, 23, 59, 59)
    assert datetime.now() == expect
