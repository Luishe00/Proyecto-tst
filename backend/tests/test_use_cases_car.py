from unittest.mock import Mock

from application.use_cases.car_use_cases import CarUseCases
from domain.entities.car import Car
from infrastructure.persistence.in_memory_car_repository import InMemoryCarRepository


def _make_repo() -> InMemoryCarRepository:
    repo = InMemoryCarRepository()
    repo.create(
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
    repo.create(
        Car(
            id=2,
            marca="Ferrari",
            modelo="Roma",
            cv=620,
            peso=1472,
            velocidad_max=320,
            precio=222000,
            imagen_url="img2",
            year=2021,
        )
    )
    repo.create(
        Car(
            id=3,
            marca="McLaren",
            modelo="P1",
            cv=916,
            peso=1395,
            velocidad_max=350,
            precio=1150000,
            imagen_url="img3",
            year=2018,
        )
    )
    return repo


def test_get_all_cars_filters_apply_independently() -> None:
    uc = CarUseCases(_make_repo())

    assert len(uc.get_all_cars(marca="Ferrari")) == 1
    assert len(uc.get_all_cars(velocidad_max=330)) == 1
    assert len(uc.get_all_cars(cv=900)) == 1
    assert len(uc.get_all_cars(precio_min=1_000_000)) == 1
    assert len(uc.get_all_cars(precio_max=230_000)) == 1
    assert len(uc.get_all_cars(year=2021)) == 1
    assert len(uc.get_all_cars(year_min=2020)) == 2


def test_create_car_without_image_storage_uses_given_url() -> None:
    repo = _make_repo()
    uc = CarUseCases(repo)

    created = uc.create_car(
        {
            "marca": "Aston Martin",
            "modelo": "DB11",
            "cv": 630,
            "peso": 1760,
            "velocidad_max": 335,
            "precio": 220000,
            "imagen_url": "http://manual",
            "year": 2019,
        }
    )

    assert created.id > 0
    assert created.imagen_url == "http://manual"


def test_create_car_with_image_storage_uploads_binary() -> None:
    repo = _make_repo()
    image_storage = Mock()
    image_storage.upload_image.return_value = "https://res.cloudinary.com/test/image.jpg"
    uc = CarUseCases(repo, image_storage=image_storage)

    created = uc.create_car(
        {
            "marca": "Bugatti",
            "modelo": "Chiron",
            "cv": 1500,
            "peso": 1995,
            "velocidad_max": 420,
            "precio": 3200000,
            "imagen_url": "",
            "year": 2024,
        },
        image_file=b"fake-bytes",
        image_filename="bugatti_chiron",
    )

    image_storage.upload_image.assert_called_once_with(b"fake-bytes", "bugatti_chiron")
    assert created.imagen_url == "https://res.cloudinary.com/test/image.jpg"


def test_update_and_delete_non_existing_car() -> None:
    uc = CarUseCases(_make_repo())

    assert uc.update_car(999, {"precio": 10}) is None
    assert uc.delete_car(999) is False
