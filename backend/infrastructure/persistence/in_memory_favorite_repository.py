"""
Adaptador de persistencia en memoria para el repositorio de favoritos.
Implementa FavoriteRepository usando una lista de Python como almacén.
"""
from typing import List, Optional

from domain.entities.favorite import Favorite
from domain.ports.favorite_repository import FavoriteRepository


class InMemoryFavoriteRepository(FavoriteRepository):
    """Repositorio de favoritos en memoria. 100% portable, sin dependencias externas."""

    def __init__(self) -> None:
        self._storage: List[Favorite] = []
        self._next_id: int = 1

    def get_by_user(self, user_id: int) -> List[Favorite]:
        """Devuelve todos los favoritos del usuario indicado."""
        return [fav for fav in self._storage if fav.user_id == user_id]

    def add(self, favorite: Favorite) -> Favorite:
        """Añade un nuevo favorito y le asigna un ID único."""
        new_favorite = Favorite(
            id=self._next_id,
            user_id=favorite.user_id,
            car_id=favorite.car_id,
        )
        self._storage.append(new_favorite)
        self._next_id += 1
        return new_favorite

    def remove(self, user_id: int, car_id: int) -> bool:
        """Elimina el favorito del usuario para el coche indicado."""
        for i, fav in enumerate(self._storage):
            if fav.user_id == user_id and fav.car_id == car_id:
                self._storage.pop(i)
                return True
        return False

    def exists(self, user_id: int, car_id: int) -> bool:
        """Comprueba si el coche ya está en favoritos del usuario."""
        return any(
            fav.user_id == user_id and fav.car_id == car_id
            for fav in self._storage
        )
