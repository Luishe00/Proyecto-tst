"""
Casos de uso para la gestión del catálogo de coches.
Contiene la lógica de negocio para operaciones CRUD y filtrado de coches.
"""
from typing import Dict, List, Optional

from domain.entities.car import Car
from domain.ports.car_repository import CarRepository


class CarUseCases:
    """Implementa los casos de uso relacionados con el catálogo de coches."""

    def __init__(self, repository: CarRepository) -> None:
        self._repository = repository

    def get_all_cars(
        self,
        marca: Optional[str] = None,
        velocidad_max: Optional[int] = None,
        cv: Optional[int] = None,
        precio_min: Optional[float] = None,
        precio_max: Optional[float] = None,
        year: Optional[int] = None,
        year_min: Optional[int] = None,
    ) -> List[Car]:
        """
        Obtiene todos los coches aplicando filtros opcionales.

        Args:
            marca: Filtrar por nombre de marca (insensible a mayúsculas).
            velocidad_max: Velocidad máxima mínima en km/h (coches con v_max >= valor).
            cv: Caballos de vapor mínimos (coches con cv >= valor).
            precio_min: Precio mínimo en euros.
            precio_max: Precio máximo en euros.
            year: Año de fabricación exacto.
            year_min: Año de fabricación mínimo (coches con year >= valor).

        Returns:
            Lista de coches que cumplen todos los filtros indicados.
        """
        cars = self._repository.get_all()

        if marca:
            cars = [c for c in cars if c.marca.lower() == marca.lower()]
        if velocidad_max is not None:
            cars = [c for c in cars if c.velocidad_max >= velocidad_max]
        if cv is not None:
            cars = [c for c in cars if c.cv >= cv]
        if precio_min is not None:
            cars = [c for c in cars if c.precio >= precio_min]
        if precio_max is not None:
            cars = [c for c in cars if c.precio <= precio_max]
        if year is not None:
            cars = [c for c in cars if c.year == year]
        if year_min is not None:
            cars = [c for c in cars if c.year >= year_min]

        return cars

    def get_car_by_id(self, car_id: int) -> Optional[Car]:
        """Obtiene un coche por su ID."""
        return self._repository.get_by_id(car_id)

    def create_car(self, car_data: Dict) -> Car:
        """
        Crea un nuevo coche en el catálogo.

        Args:
            car_data: Diccionario con los campos del coche (sin ID).

        Returns:
            El coche recién creado con su ID asignado.
        """
        new_car = Car(**car_data)
        return self._repository.create(new_car)

    def update_car(self, car_id: int, data: Dict) -> Optional[Car]:
        """
        Actualiza los campos de un coche existente.

        Args:
            car_id: ID del coche a actualizar.
            data: Diccionario con los campos a modificar.

        Returns:
            El coche actualizado, o None si no existe.
        """
        filtered_data = {k: v for k, v in data.items() if v is not None}
        return self._repository.update(car_id, filtered_data)

    def delete_car(self, car_id: int) -> bool:
        """
        Elimina un coche del catálogo.

        Args:
            car_id: ID del coche a eliminar.

        Returns:
            True si fue eliminado, False si no existía.
        """
        return self._repository.delete(car_id)
