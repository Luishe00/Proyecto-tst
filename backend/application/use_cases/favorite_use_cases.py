"""
Casos de uso para la gestión de favoritos de usuario.
Permite añadir, consultar y eliminar coches de la lista de favoritos.
"""
from typing import List

from domain.entities.car import Car
from domain.entities.favorite import Favorite
from domain.ports.car_repository import CarRepository
from domain.ports.favorite_repository import FavoriteRepository


class FavoriteUseCases:
    """Implementa los casos de uso relacionados con los favoritos de usuario."""

    def __init__(
        self,
        favorite_repository: FavoriteRepository,
        car_repository: CarRepository,
    ) -> None:
        self._favorite_repository = favorite_repository
        self._car_repository = car_repository

    def get_favorites(self, user_id: int) -> List[Car]:
        """
        Obtiene la lista de coches favoritos de un usuario.

        Args:
            user_id: ID del usuario.

        Returns:
            Lista de objetos Car correspondientes a los favoritos del usuario.
        """
        favorites = self._favorite_repository.get_by_user(user_id)
        cars: List[Car] = []
        for fav in favorites:
            car = self._car_repository.get_by_id(fav.car_id)
            if car:
                cars.append(car)
        return cars

    def add_favorite(self, user_id: int, car_id: int) -> Favorite:
        """
        Añade un coche a la lista de favoritos del usuario.

        Args:
            user_id: ID del usuario.
            car_id: ID del coche a añadir.

        Returns:
            El objeto Favorite recién creado.

        Raises:
            ValueError: Si el coche no existe o ya está en favoritos.
        """
        car = self._car_repository.get_by_id(car_id)
        if not car:
            raise ValueError(f"El coche con ID {car_id} no existe en el catálogo.")
        if self._favorite_repository.exists(user_id, car_id):
            raise ValueError("Este coche ya está en tu lista de favoritos.")
        new_favorite = Favorite(user_id=user_id, car_id=car_id)
        return self._favorite_repository.add(new_favorite)

    def remove_favorite(self, user_id: int, car_id: int) -> bool:
        """
        Elimina un coche de la lista de favoritos del usuario.

        Args:
            user_id: ID del usuario.
            car_id: ID del coche a eliminar.

        Returns:
            True si se eliminó correctamente.

        Raises:
            ValueError: Si el coche no estaba en favoritos.
        """
        if not self._favorite_repository.exists(user_id, car_id):
            raise ValueError("Este coche no está en tu lista de favoritos.")
        return self._favorite_repository.remove(user_id, car_id)
