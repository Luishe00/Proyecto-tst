"""
Puerto (interfaz abstracta) para el repositorio de coches.
Define el contrato que deben cumplir todos los adaptadores de persistencia de coches.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from domain.entities.car import Car


class CarRepository(ABC):
    """Interfaz abstracta que define las operaciones de persistencia para coches."""

    @abstractmethod
    def get_all(self) -> List[Car]:
        """Obtiene todos los coches del catálogo."""
        ...

    @abstractmethod
    def get_by_id(self, car_id: int) -> Optional[Car]:
        """Obtiene un coche por su ID. Devuelve None si no existe."""
        ...

    @abstractmethod
    def create(self, car: Car) -> Car:
        """Crea un nuevo coche y lo persiste. Devuelve el coche con su ID asignado."""
        ...

    @abstractmethod
    def update(self, car_id: int, data: Dict) -> Optional[Car]:
        """Actualiza los campos indicados de un coche. Devuelve None si no existe."""
        ...

    @abstractmethod
    def delete(self, car_id: int) -> bool:
        """Elimina un coche por su ID. Devuelve True si fue eliminado, False si no existía."""
        ...
