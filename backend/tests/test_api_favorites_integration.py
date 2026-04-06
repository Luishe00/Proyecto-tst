import pytest


pytestmark = pytest.mark.anyio


async def test_favorite_decision_table_success(async_client, user_token: str) -> None:
    resp = await async_client.post(
        "/me/favorites/1",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 201


async def test_favorite_decision_table_duplicate(async_client, user_token: str) -> None:
    first = await async_client.post(
        "/me/favorites/1",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert first.status_code == 201

    second = await async_client.post(
        "/me/favorites/1",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert second.status_code == 409


async def test_favorite_decision_table_anonymous(async_client) -> None:
    resp = await async_client.post("/me/favorites/1")
    assert resp.status_code == 401


async def test_favorite_delete_existing_and_non_existing(async_client, user_token: str) -> None:
    added = await async_client.post(
        "/me/favorites/1",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert added.status_code == 201

    deleted = await async_client.delete(
        "/me/favorites/1",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert deleted.status_code == 200

    missing = await async_client.delete(
        "/me/favorites/1",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert missing.status_code == 404


async def test_favorite_non_existing_car(async_client, user_token: str) -> None:
    resp = await async_client.post(
        "/me/favorites/999",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 409


async def test_get_favorites_requires_auth(async_client) -> None:
    resp = await async_client.get("/me/favorites")
    assert resp.status_code == 401


async def test_get_favorites_returns_created_items(async_client, user_token: str) -> None:
    added = await async_client.post(
        "/me/favorites/1",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert added.status_code == 201

    favorites = await async_client.get(
        "/me/favorites",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert favorites.status_code == 200
    body = favorites.json()
    assert len(body) == 1
    assert body[0]["id"] == 1
