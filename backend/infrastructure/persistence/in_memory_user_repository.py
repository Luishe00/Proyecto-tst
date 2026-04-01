"""
Adaptador de persistencia en memoria para el repositorio de usuarios.
Implementa UserRepository usando un diccionario de Python como almacén.
"""
from typing import Dict, List, Optional

from domain.entities.user import User
from domain.ports.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    """Repositorio de usuarios en memoria. 100% portable, sin dependencias externas."""

    def __init__(self) -> None:
        self._storage: Dict[int, User] = {}
        self._next_id: int = 1

    def get_by_username(self, username: str) -> Optional[User]:
        """Busca un usuario por nombre de usuario (sensible a mayúsculas)."""
        for user in self._storage.values():
            if user.username == username:
                return user
        return None

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Devuelve el usuario con el ID indicado o None si no existe."""
        return self._storage.get(user_id)

    def create(self, user: User) -> User:
        """
        Persiste un usuario nuevo.
        Si user.id > 0 (seed data), usa ese ID.
        Si user.id == 0, asigna el siguiente ID disponible.
        """
        if user.id > 0:
            self._storage[user.id] = user
            if user.id >= self._next_id:
                self._next_id = user.id + 1
            return user
        stored_user = user.model_copy(update={"id": self._next_id})
        self._storage[self._next_id] = stored_user
        self._next_id += 1
        return stored_user
