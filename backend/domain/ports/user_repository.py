"""
Puerto (interfaz abstracta) para el repositorio de usuarios.
Define el contrato para las operaciones de persistencia de usuarios.
"""
from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.user import User


class UserRepository(ABC):
    """Interfaz abstracta que define las operaciones de persistencia para usuarios."""

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """Busca un usuario por su nombre de usuario. Devuelve None si no existe."""
        ...

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Busca un usuario por su ID. Devuelve None si no existe."""
        ...

    @abstractmethod
    def create(self, user: User) -> User:
        """Crea un nuevo usuario y lo persiste. Devuelve el usuario con su ID asignado."""
        ...
