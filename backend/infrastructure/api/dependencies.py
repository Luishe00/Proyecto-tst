"""
Dependencias de seguridad para FastAPI.
Provee funciones reutilizables para extraer y validar el usuario actual
desde el token JWT en los encabezados de la petición.
"""
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from application.use_cases.auth_use_cases import AuthUseCases
from domain.entities.user import Role, User
from infrastructure.api.container import get_auth_use_cases, get_jwt_handler
from infrastructure.auth.jwt_handler import JWTHandler

# auto_error=False permite que el token sea opcional (usuarios anónimos)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


def get_optional_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
    auth_uc: AuthUseCases = Depends(get_auth_use_cases),
) -> Optional[User]:
    """
    Intenta obtener el usuario actual a partir del token JWT.
    Devuelve None si no hay token o si es inválido (sin lanzar error).
    """
    if not token:
        return None
    try:
        payload = jwt_handler.decode_token(token)
        username: Optional[str] = payload.get("sub")
        if not username:
            return None
        return auth_uc.get_user_by_username(username)
    except JWTError:
        return None


def get_current_user(
    current_user: Optional[User] = Depends(get_optional_current_user),
) -> User:
    """
    Obtiene el usuario autenticado. Lanza HTTP 401 si no hay sesión activa.
    """
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado. Por favor, inicia sesión para acceder a este recurso.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="La cuenta de usuario está inactiva.",
        )
    return current_user


def get_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Verifica que el usuario autenticado tenga rol de administrador.
    Lanza HTTP 403 si no tiene permisos suficientes.
    """
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requieren permisos de administrador.",
        )
    return current_user
