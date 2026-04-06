from application.use_cases.auth_use_cases import AuthUseCases
from application.use_cases.car_use_cases import CarUseCases
from application.use_cases.favorite_use_cases import FavoriteUseCases
from infrastructure.api.container import (
    get_auth_use_cases,
    get_car_repository,
    get_car_use_cases,
    get_favorite_use_cases,
    get_jwt_handler,
)
from infrastructure.auth.jwt_handler import JWTHandler
from infrastructure.persistence.in_memory_car_repository import InMemoryCarRepository


def test_container_factories_return_expected_types() -> None:
    assert isinstance(get_car_repository(), InMemoryCarRepository)
    assert isinstance(get_car_use_cases(), CarUseCases)
    assert isinstance(get_auth_use_cases(), AuthUseCases)
    assert isinstance(get_favorite_use_cases(), FavoriteUseCases)
    assert isinstance(get_jwt_handler(), JWTHandler)


def test_container_singletons_are_stable_across_calls() -> None:
    assert get_car_repository() is get_car_repository()
    assert get_jwt_handler() is get_jwt_handler()
