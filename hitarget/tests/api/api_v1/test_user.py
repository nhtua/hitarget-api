from fastapi.testclient import TestClient

from hitarget.core.config import settings


def test_create_user(client: TestClient):
    user_data = dict(
        email="someone@email.com",
        password="password",
    )
    response = client.post(f"{settings.API_V1_PREFIX}/users", json=user_data)
    r_user = response.json()

    assert response.status_code == 201
    assert 'password' not in r_user
    assert 'id' in r_user
    assert r_user['email'] == user_data['email']
    assert r_user['name'] is None
