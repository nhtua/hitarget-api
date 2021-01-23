import pytest

from hitarget.core.config import settings
from tests.conftest import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_health_check(client: AsyncClient):
    response = await client.get(f"{settings.API_V1_PREFIX}/health")
    assert response.status_code == 200
    assert response.json() == dict(health="OK")
