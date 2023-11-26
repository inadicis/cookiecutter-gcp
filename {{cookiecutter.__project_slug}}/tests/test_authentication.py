import pytest
from starlette.testclient import TestClient

from src.authentication import admin_jwt, alien_jwt

admin_auth0_id = admin_jwt.auth0_id()


@pytest.fixture()
async def client_unauthenticated(app) -> TestClient:
    with TestClient(app=app, base_url="http://test") as ac:
        yield ac


# logged in clients
@pytest.fixture()
async def client_authenticated(app) -> TestClient:
    headers = {"Authorization": f"Bearer {alien_jwt.get_signed_jwt()}"}
    with TestClient(app=app, base_url="http://test", headers=headers) as ac:
        yield ac


@pytest.mark.parametrize(
    ["url", "unauthenticated_expected_status", "authenticated_expected_status",
     "admin_expected_status"],
    [
        ("/tests/openroute/", 200, 200, 200),
        ("/tests/authenticated/", 403, 200, 200),
        ("/tests/permission/", 403, 401, 200),
    ]
)
@pytest.mark.asyncio
async def test_authentication(
        client, client_authenticated, client_unauthenticated, url, unauthenticated_expected_status,
        authenticated_expected_status, admin_expected_status

):

    response = client_unauthenticated.get(url)
    assert response.status_code == unauthenticated_expected_status

    response = client_authenticated.get(url)
    assert response.status_code == authenticated_expected_status

    response = client.get(url)
    assert response.status_code == admin_expected_status
