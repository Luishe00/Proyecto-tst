"""
Puerto (interfaz abstracta) para el repositorio de favoritos.
Define el contrato para las operaciones de persistencia de favoritos de usuario.
"""
from abc import ABC, abstractmethod
from typing import List

from domain.entities.favorite import Favorite


class FavoriteRepository(ABC):
    """Interfaz abstracta que define las operaciones de persistencia para favoritos."""

    @abstractmethod
    def get_by_user(self, user_id: int) -> List[Favorite]:
        """Obtiene todos los favoritos de un usuario."""
        ...

    @abstractmethod
    def add(self, favorite: Favorite) -> Favorite:
        """Añade un coche a favoritos de un usuario. Devuelve el favorito con ID asignado."""
        ...

    @abstractmethod
    def remove(self, user_id: int, car_id: int) -> bool:
        """Elimina un coche de favoritos de un usuario. Devuelve True si se eliminó."""
        ...

    @abstractmethod
    def exists(self, user_id: int, car_id: int) -> bool:
        """Comprueba si un coche ya está en favoritos del usuario."""
        ...
