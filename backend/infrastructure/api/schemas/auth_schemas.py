"""
Esquemas Pydantic para los endpoints de autenticación.
"""
from pydantic import BaseModel


class TokenResponse(BaseModel):
    """Respuesta del endpoint de login con el token JWT."""

    access_token: str
    token_type: str = "bearer"


class UserInfoResponse(BaseModel):
    """Información básica del usuario autenticado."""

    id: int
    username: str
    role: str
