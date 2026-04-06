import pytest


pytestmark = pytest.mark.anyio


async def test_get_cars_public_vs_authenticated(async_client, user_token: str) -> None:
    public_resp = await async_client.get("/cars")
    assert public_resp.status_code == 200
    public_item = public_resp.json()[0]
    assert set(public_item.keys()) == {"id", "marca", "modelo", "imagen_url"}

    auth_resp = await async_client.get(
        "/cars",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert auth_resp.status_code == 200
    auth_item = auth_resp.json()[0]
    assert {"cv", "precio", "year"}.issubset(auth_item.keys())


async def test_get_car_requires_auth(async_client) -> None:
    resp = await async_client.get("/cars/1")
    assert resp.status_code == 401


async def test_create_car_admin_only(async_client, user_token: str) -> None:
    resp = await async_client.post(
        "/cars",
        headers={"Authorization": f"Bearer {user_token}"},
        data={
            "marca": "Bugatti",
            "modelo": "Chiron",
            "cv": 1500,
            "peso": 1995,
            "velocidad_max": 420,
            "precio": 3200000,
            "year": 2024,
            "imagen_url": "https://example.com/chiron.jpg",
        },
    )
    assert resp.status_code == 403


async def test_create_car_with_file_uses_mocked_cloudinary(async_client, admin_token: str) -> None:
    resp = await async_client.post(
        "/cars",
        headers={"Authorization": f"Bearer {admin_token}"},
        data={
            "marca": "Bugatti",
            "modelo": "Chiron",
            "cv": 1500,
            "peso": 1995,
            "velocidad_max": 420,
            "precio": 3200000,
            "year": 2024,
        },
        files={"imagen": ("chiron.jpg", b"fake-image-content", "image/jpeg")},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["imagen_url"] == "https://res.cloudinary.com/test/image.jpg"


async def test_create_car_requires_image_or_url(async_client, admin_token: str) -> None:
    resp = await async_client.post(
        "/cars",
        headers={"Authorization": f"Bearer {admin_token}"},
        data={
            "marca": "Lotus",
            "modelo": "Emira",
            "cv": 400,
            "peso": 1405,
            "velocidad_max": 290,
            "precio": 98000,
            "year": 2024,
        },
    )
    assert resp.status_code == 422


async def test_update_delete_and_not_found_flows(async_client, admin_token: str) -> None:
    created = await async_client.post(
        "/cars",
        headers={"Authorization": f"Bearer {admin_token}"},
        data={
            "marca": "Aston Martin",
            "modelo": "Vantage",
            "cv": 665,
            "peso": 1650,
            "velocidad_max": 325,
            "precio": 190000,
            "year": 2024,
            "imagen_url": "https://example.com/vantage.jpg",
        },
    )
    assert created.status_code == 201
    car_id = created.json()["id"]

    updated = await async_client.put(
        f"/cars/{car_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"precio": 195000},
    )
    assert updated.status_code == 200
    assert updated.json()["precio"] == 195000

    missing_update = await async_client.put(
        "/cars/9999",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"precio": 1},
    )
    assert missing_update.status_code == 404

    deleted = await async_client.delete(
        f"/cars/{car_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert deleted.status_code == 200

    missing_delete = await async_client.delete(
        "/cars/9999",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert missing_delete.status_code == 404


async def test_get_car_not_found(async_client, admin_token: str) -> None:
    resp = await async_client.get(
        "/cars/9999",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 404


@pytest.mark.parametrize(
    "query, expected_status",
    [
        ({"year": 1885}, 422),
        ({"precio_min": -1}, 422),
        ({"cv": 0}, 422),
    ],
)
async def test_get_cars_query_validation_errors(async_client, query: dict, expected_status: int) -> None:
    resp = await async_client.get("/cars", params=query)
    assert resp.status_code == expected_status


async def test_create_car_validation_missing_required_field(async_client, admin_token: str) -> None:
    # Falta marca (campo obligatorio)
    resp = await async_client.post(
        "/cars",
        headers={"Authorization": f"Bearer {admin_token}"},
        data={
            "modelo": "Chiron",
            "cv": 1500,
            "peso": 1995,
            "velocidad_max": 420,
            "precio": 3200000,
            "year": 2024,
            "imagen_url": "https://example.com/chiron.jpg",
        },
    )
    assert resp.status_code == 422


async def test_create_car_validation_invalid_numeric_type(async_client, admin_token: str) -> None:
    # cv inválido para disparar validación de tipo
    resp = await async_client.post(
        "/cars",
        headers={"Authorization": f"Bearer {admin_token}"},
        data={
            "marca": "Bugatti",
            "modelo": "Chiron",
            "cv": "invalid",
            "peso": 1995,
            "velocidad_max": 420,
            "precio": 3200000,
            "year": 2024,
            "imagen_url": "https://example.com/chiron.jpg",
        },
    )
    assert resp.status_code == 422


@pytest.mark.parametrize(
    "payload, expected_status",
    [
        (
            {
                "marca": "Bugatti",
                "modelo": "PriceZero",
                "cv": 100,
                "peso": 1000,
                "velocidad_max": 200,
                "precio": 0,
                "year": 2024,
                "imagen_url": "https://example.com/a.jpg",
            },
            422,
        ),
        (
            {
                "marca": "Bugatti",
                "modelo": "PriceNegative",
                "cv": 100,
                "peso": 1000,
                "velocidad_max": 200,
                "precio": -1,
                "year": 2024,
                "imagen_url": "https://example.com/a.jpg",
            },
            422,
        ),
        (
            {
                "marca": "Bugatti",
                "modelo": "PriceOne",
                "cv": 100,
                "peso": 1000,
                "velocidad_max": 200,
                "precio": 1,
                "year": 2024,
                "imagen_url": "https://example.com/a.jpg",
            },
            201,
        ),
        (
            {
                "marca": "Bugatti",
                "modelo": "CvZero",
                "cv": 0,
                "peso": 1000,
                "velocidad_max": 200,
                "precio": 1,
                "year": 2024,
                "imagen_url": "https://example.com/a.jpg",
            },
            422,
        ),
        (
            {
                "marca": "Bugatti",
                "modelo": "CvOne",
                "cv": 1,
                "peso": 1000,
                "velocidad_max": 200,
                "precio": 1,
                "year": 2024,
                "imagen_url": "https://example.com/a.jpg",
            },
            201,
        ),
        (
            {
                "marca": "Bugatti",
                "modelo": "CvMaxFail",
                "cv": 2001,
                "peso": 1000,
                "velocidad_max": 200,
                "precio": 1,
                "year": 2024,
                "imagen_url": "https://example.com/a.jpg",
            },
            422,
        ),
        (
            {
                "marca": "Bugatti",
                "modelo": "YearLowerFail",
                "cv": 100,
                "peso": 1000,
                "velocidad_max": 200,
                "precio": 1,
                "year": 1885,
                "imagen_url": "https://example.com/a.jpg",
            },
            422,
        ),
        (
            {
                "marca": "Bugatti",
                "modelo": "YearLowerOk",
                "cv": 100,
                "peso": 1000,
                "velocidad_max": 200,
                "precio": 1,
                "year": 1886,
                "imagen_url": "https://example.com/a.jpg",
            },
            201,
        ),
        (
            {
                "marca": "Bugatti",
                "modelo": "YearUpperFail",
                "cv": 100,
                "peso": 1000,
                "velocidad_max": 200,
                "precio": 1,
                "year": 2028,
                "imagen_url": "https://example.com/a.jpg",
            },
            422,
        ),
    ],
)
async def test_create_car_equivalence_classes(async_client, admin_token: str, payload: dict, expected_status: int) -> None:
    resp = await async_client.post(
        "/cars",
        headers={"Authorization": f"Bearer {admin_token}"},
        data=payload,
    )
    assert resp.status_code == expected_status
