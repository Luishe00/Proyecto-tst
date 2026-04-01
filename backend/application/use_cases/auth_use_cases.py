"""
Casos de uso para la autenticación de usuarios.
Gestiona la verificación de credenciales y la consulta de usuarios.
"""
from typing import Optional

from passlib.context import CryptContext

from domain.entities.user import User
from domain.ports.user_repository import UserRepository

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthUseCases:
    """Implementa los casos de uso de autenticación."""

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Verifica las credenciales del usuario.

        Args:
            username: Nombre de usuario.
            password: Contraseña en texto plano.

        Returns:
            El objeto User si las credenciales son correctas y la cuenta está activa,
            None en caso contrario.
        """
        user = self._repository.get_by_username(username)
        if not user or not user.is_active:
            return None
        if not _pwd_context.verify(password, user.hashed_password):
            return None
        return user

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Busca un usuario por su nombre de usuario."""
        return self._repository.get_by_username(username)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Busca un usuario por su ID."""
        return self._repository.get_by_id(user_id)

    @staticmethod
    def hash_password(plain_password: str) -> str:
        """Genera el hash bcrypt de una contraseña en texto plano."""
        return _pwd_context.hash(plain_password)
