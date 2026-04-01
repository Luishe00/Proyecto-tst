"""
Adaptador de persistencia en memoria para el repositorio de coches.
Implementa CarRepository usando un diccionario de Python como almacén.
"""
from typing import Dict, List, Optional

from domain.entities.car import Car
from domain.ports.car_repository import CarRepository


class InMemoryCarRepository(CarRepository):
    """Repositorio de coches en memoria. 100% portable, sin dependencias externas."""

    def __init__(self) -> None:
        self._storage: Dict[int, Car] = {}
        self._next_id: int = 1

    def get_all(self) -> List[Car]:
        """Devuelve todos los coches almacenados."""
        return list(self._storage.values())

    def get_by_id(self, car_id: int) -> Optional[Car]:
        """Devuelve el coche con el ID indicado o None si no existe."""
        return self._storage.get(car_id)

    def create(self, car: Car) -> Car:
        """
        Persiste un coche nuevo.
        Si car.id > 0 (seed data), usa ese ID.
        Si car.id == 0, asigna el siguiente ID disponible.
        """
        if car.id > 0:
            stored_car = car
            self._storage[car.id] = stored_car
            if car.id >= self._next_id:
                self._next_id = car.id + 1
        else:
            stored_car = car.model_copy(update={"id": self._next_id})
            self._storage[self._next_id] = stored_car
            self._next_id += 1
        return stored_car

    def update(self, car_id: int, data: Dict) -> Optional[Car]:
        """Actualiza los campos indicados de un coche. Devuelve el coche actualizado o None."""
        if car_id not in self._storage:
            return None
        updated_car = self._storage[car_id].model_copy(update=data)
        self._storage[car_id] = updated_car
        return updated_car

    def delete(self, car_id: int) -> bool:
        """Elimina un coche por ID. Devuelve True si existía y fue eliminado."""
        if car_id not in self._storage:
            return False
        del self._storage[car_id]
        return True
