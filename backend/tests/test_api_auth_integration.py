import pytest


pytestmark = pytest.mark.anyio


async def test_login_invalid_credentials_returns_401(async_client) -> None:
    resp = await async_client.post(
        "/auth/login",
        data={"username": "admin", "password": "bad-password"},
    )
    assert resp.status_code == 401


async def test_get_me_requires_auth(async_client) -> None:
    resp = await async_client.get("/auth/me")
    assert resp.status_code == 401


async def test_get_me_returns_current_user(async_client, user_token: str) -> None:
    resp = await async_client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["username"] == "user"
    assert body["role"] == "user"
