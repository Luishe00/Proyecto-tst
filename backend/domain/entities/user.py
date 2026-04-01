"""
Entidad de dominio: Usuario.
Representa un usuario del sistema con su rol y credenciales.
"""
from enum import Enum

from pydantic import BaseModel, Field


class Role(str, Enum):
    """Roles disponibles en el sistema."""

    ADMIN = "admin"
    USER = "user"


class User(BaseModel):
    """Entidad que representa un usuario del sistema."""

    id: int = Field(default=0, description="Identificador único del usuario")
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario")
    hashed_password: str = Field(..., description="Contraseña hasheada con bcrypt")
    role: Role = Field(default=Role.USER, description="Rol del usuario en el sistema")
    is_active: bool = Field(default=True, description="Indica si la cuenta está activa")

    model_config = {"from_attributes": True}
