from domain.entities.car import Car
from domain.entities.favorite import Favorite
from domain.entities.user import Role, User
from infrastructure.persistence.in_memory_car_repository import InMemoryCarRepository
from infrastructure.persistence.in_memory_favorite_repository import InMemoryFavoriteRepository
from infrastructure.persistence.in_memory_user_repository import InMemoryUserRepository


def test_in_memory_user_repository_create_get_by_id_and_username() -> None:
    repo = InMemoryUserRepository()

    created = repo.create(
        User(
            username="new_user",
            hashed_password="hash",
            role=Role.USER,
            is_active=True,
        )
    )

    assert created.id == 1
    assert repo.get_by_id(1) is not None
    assert repo.get_by_username("new_user") is not None


def test_in_memory_car_repository_crud() -> None:
    repo = InMemoryCarRepository()

    created = repo.create(
        Car(
            marca="Ferrari",
            modelo="F8",
            cv=720,
            peso=1330,
            velocidad_max=340,
            precio=276000,
            imagen_url="img",
            year=2020,
        )
    )
    assert created.id == 1

    updated = repo.update(created.id, {"precio": 280000})
    assert updated is not None
    assert updated.precio == 280000

    assert repo.delete(created.id) is True
    assert repo.delete(created.id) is False


def test_in_memory_car_repository_edge_cases_seed_and_missing_ids() -> None:
    repo = InMemoryCarRepository(load_seed=True)

    # Edge case: seed completo en memoria
    cars = repo.get_all()
    assert len(cars) == 25
    assert repo.get_by_id(1) is not None
    assert repo.get_by_id(25) is not None

    # Edge case: IDs inexistentes
    assert repo.get_by_id(99999) is None
    assert repo.update(99999, {"precio": 1}) is None

    # Edge case: tras seed, el siguiente ID autogenerado debe ser 26
    created = repo.create(
        Car(
            marca="Test",
            modelo="AfterSeed",
            cv=100,
            peso=1200,
            velocidad_max=200,
            precio=10000,
            imagen_url="img",
            year=2020,
        )
    )
    assert created.id == 26


def test_in_memory_favorite_repository_methods() -> None:
    repo = InMemoryFavoriteRepository()

    added = repo.add(Favorite(user_id=3, car_id=9))
    assert added.id == 1
    assert repo.exists(3, 9) is True
    assert len(repo.get_by_user(3)) == 1
    assert repo.remove(3, 9) is True
    assert repo.remove(3, 9) is False
