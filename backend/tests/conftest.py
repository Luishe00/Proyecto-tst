from __future__ import annotations

from dataclasses import dataclass
from typing import AsyncGenerator, Generator
from unittest.mock import patch

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from application.use_cases.auth_use_cases import AuthUseCases
from application.use_cases.car_use_cases import CarUseCases
from application.use_cases.favorite_use_cases import FavoriteUseCases
from domain.entities.car import Car
from domain.entities.user import Role, User
from infrastructure.api.container import (
    get_auth_use_cases,
    get_car_use_cases,
    get_favorite_use_cases,
    get_jwt_handler,
)
from infrastructure.api.routers import auth, cars, favorites
from infrastructure.adapters.cloudinary_adapter import CloudinaryAdapter
from infrastructure.auth.jwt_handler import JWTHandler
from infrastructure.persistence.in_memory_car_repository import InMemoryCarRepository
from infrastructure.persistence.in_memory_favorite_repository import InMemoryFavoriteRepository
from infrastructure.persistence.in_memory_user_repository import InMemoryUserRepository


CLOUDINARY_MOCK_URL = "https://res.cloudinary.com/test/image.jpg"


@dataclass
class TestState:
    car_repo: InMemoryCarRepository
    user_repo: InMemoryUserRepository
    favorite_repo: InMemoryFavoriteRepository
    car_uc: CarUseCases
    auth_uc: AuthUseCases
    favorite_uc: FavoriteUseCases
    jwt_handler: JWTHandler


@pytest.fixture(autouse=True)
def mock_cloudinary_upload() -> Generator[None, None, None]:
    """Aisla todos los tests de servicios externos de imágenes."""
    with patch(
        "infrastructure.adapters.cloudinary_adapter.CloudinaryAdapter.upload_image",
        return_value=CLOUDINARY_MOCK_URL,
    ):
        yield


@pytest.fixture(scope="function")
def test_state() -> TestState:
    """Infraestructura efímera por test para garantizar independencia total."""
    # Crear repositorios SIN cargar los 25 coches del seed (para aislamiento en tests)
    car_repo = InMemoryCarRepository(load_seed=False)
    user_repo = InMemoryUserRepository()
    favorite_repo = InMemoryFavoriteRepository()

    car_repo.create(
        Car(
            id=1,
            marca="Porsche",
            modelo="911 GT3 RS",
            cv=525,
            peso=1450,
            velocidad_max=296,
            precio=239700,
            imagen_url="https://placehold.jp/24/003366/ffffff/1280x720.png?text=Porsche_911_GT3_RS",
            year=2022,
        )
    )
    car_repo.create(
        Car(
            id=2,
            marca="Ferrari",
            modelo="Roma",
            cv=620,
            peso=1472,
            velocidad_max=320,
            precio=222000,
            imagen_url="https://placehold.jp/24/cc0000/ffffff/1280x720.png?text=Ferrari_Roma",
            year=2021,
        )
    )

    user_repo.create(
        User(
            id=1,
            username="admin",
            hashed_password=AuthUseCases.hash_password("Admin1234!"),
            role=Role.ADMIN,
            is_active=True,
        )
    )
    user_repo.create(
        User(
            id=2,
            username="user",
            hashed_password=AuthUseCases.hash_password("User1234!"),
            role=Role.USER,
            is_active=True,
        )
    )

    jwt_handler = JWTHandler()
    auth_uc = AuthUseCases(user_repo)
    car_uc = CarUseCases(car_repo, image_storage=CloudinaryAdapter())
    favorite_uc = FavoriteUseCases(favorite_repo, car_repo)

    return TestState(
        car_repo=car_repo,
        user_repo=user_repo,
        favorite_repo=favorite_repo,
        car_uc=car_uc,
        auth_uc=auth_uc,
        favorite_uc=favorite_uc,
        jwt_handler=jwt_handler,
    )


@pytest.fixture(scope="function")
def app(test_state: TestState) -> FastAPI:
    app = FastAPI()
    app.include_router(auth.router)
    app.include_router(cars.router)
    app.include_router(favorites.router)

    app.dependency_overrides[get_auth_use_cases] = lambda: test_state.auth_uc
    app.dependency_overrides[get_car_use_cases] = lambda: test_state.car_uc
    app.dependency_overrides[get_favorite_use_cases] = lambda: test_state.favorite_uc
    app.dependency_overrides[get_jwt_handler] = lambda: test_state.jwt_handler

    return app


@pytest.fixture(scope="function")
async def async_client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="function")
async def admin_token(async_client: AsyncClient) -> str:
    response = await async_client.post(
        "/auth/login",
        data={"username": "admin", "password": "Admin1234!"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture(scope="function")
async def user_token(async_client: AsyncClient) -> str:
    response = await async_client.post(
        "/auth/login",
        data={"username": "user", "password": "User1234!"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]
