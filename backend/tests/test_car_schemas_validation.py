from datetime import date

import pytest
from pydantic import ValidationError

from infrastructure.api.schemas.car_schemas import CarCreate, CarFullResponse, CarUpdate


def test_car_create_rejects_year_too_far_in_future() -> None:
    too_future = date.today().year + 2

    with pytest.raises(ValidationError):
        CarCreate(
            marca="Ferrari",
            modelo="F8 Tributo",
            cv=720,
            peso=1330,
            velocidad_max=340,
            precio=276000,
            imagen_url="https://example.com/f8.jpg",
            year=too_future,
        )


def test_car_full_response_rejects_year_too_far_in_future() -> None:
    too_future = date.today().year + 2

    with pytest.raises(ValidationError):
        CarFullResponse(
            id=1,
            marca="Porsche",
            modelo="911 GT3 RS",
            cv=525,
            peso=1450,
            velocidad_max=296,
            precio=239700,
            imagen_url="https://example.com/911.jpg",
            year=too_future,
        )


def test_car_full_response_accepts_boundary_year() -> None:
    boundary_year = date.today().year + 1
    payload = CarFullResponse(
        id=1,
        marca="Porsche",
        modelo="911 GT3 RS",
        cv=525,
        peso=1450,
        velocidad_max=296,
        precio=239700,
        imagen_url="https://example.com/911.jpg",
        year=boundary_year,
    )
    assert payload.year == boundary_year


def test_car_update_allows_year_none() -> None:
    payload = CarUpdate(year=None)
    assert payload.year is None


def test_car_update_rejects_year_too_far_in_future() -> None:
    too_future = date.today().year + 2

    with pytest.raises(ValidationError):
        CarUpdate(year=too_future)


def test_car_create_accepts_boundary_year() -> None:
    boundary_year = date.today().year + 1

    payload = CarCreate(
        marca="Ferrari",
        modelo="F8 Tributo",
        cv=720,
        peso=1330,
        velocidad_max=340,
        precio=276000,
        imagen_url="https://example.com/f8.jpg",
        year=boundary_year,
    )
    assert payload.year == boundary_year


def test_car_update_accepts_boundary_year() -> None:
    boundary_year = date.today().year + 1
    payload = CarUpdate(year=boundary_year)
    assert payload.year == boundary_year
