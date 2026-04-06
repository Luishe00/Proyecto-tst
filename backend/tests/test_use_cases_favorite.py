import pytest

from application.use_cases.favorite_use_cases import FavoriteUseCases
from domain.entities.car import Car
from infrastructure.persistence.in_memory_car_repository import InMemoryCarRepository
from infrastructure.persistence.in_memory_favorite_repository import InMemoryFavoriteRepository


def _repos() -> tuple[InMemoryFavoriteRepository, InMemoryCarRepository]:
    favorite_repo = InMemoryFavoriteRepository()
    car_repo = InMemoryCarRepository()
    car_repo.create(
        Car(
            id=1,
            marca="Porsche",
            modelo="911 GT3 RS",
            cv=525,
            peso=1450,
            velocidad_max=296,
            precio=239700,
            imagen_url="img1",
            year=2022,
        )
    )
    return favorite_repo, car_repo


def test_add_favorite_success() -> None:
    favorite_repo, car_repo = _repos()
    uc = FavoriteUseCases(favorite_repo, car_repo)

    fav = uc.add_favorite(user_id=10, car_id=1)

    assert fav.id == 1
    assert fav.user_id == 10
    assert fav.car_id == 1


def test_add_favorite_car_not_exists_raises() -> None:
    favorite_repo, car_repo = _repos()
    uc = FavoriteUseCases(favorite_repo, car_repo)

    with pytest.raises(ValueError):
        uc.add_favorite(user_id=10, car_id=999)


def test_add_favorite_duplicate_raises() -> None:
    favorite_repo, car_repo = _repos()
    uc = FavoriteUseCases(favorite_repo, car_repo)

    uc.add_favorite(user_id=10, car_id=1)
    with pytest.raises(ValueError):
        uc.add_favorite(user_id=10, car_id=1)


def test_remove_favorite_non_existing_raises() -> None:
    favorite_repo, car_repo = _repos()
    uc = FavoriteUseCases(favorite_repo, car_repo)

    with pytest.raises(ValueError):
        uc.remove_favorite(user_id=10, car_id=1)


def test_remove_favorite_existing_returns_true() -> None:
    favorite_repo, car_repo = _repos()
    uc = FavoriteUseCases(favorite_repo, car_repo)

    uc.add_favorite(user_id=10, car_id=1)
    assert uc.remove_favorite(user_id=10, car_id=1) is True


def test_get_favorites_ignores_orphan_entries() -> None:
    favorite_repo, car_repo = _repos()
    uc = FavoriteUseCases(favorite_repo, car_repo)

    uc.add_favorite(user_id=10, car_id=1)
    car_repo.delete(1)

    result = uc.get_favorites(user_id=10)
    assert result == []
