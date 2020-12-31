from fastapi.testclient import TestClient

from hitarget.core.config import settings


def test_health_check(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/health")
    assert response.status_code == 200
    assert response.json() == dict(health="OK")
