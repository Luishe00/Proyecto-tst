"""
Esquemas Pydantic para los endpoints de favoritos.
"""
from pydantic import BaseModel


class FavoriteResponse(BaseModel):
    """Respuesta al añadir un coche a favoritos."""

    id: int
    user_id: int
    car_id: int

    model_config = {"from_attributes": True}


class MessageResponse(BaseModel):
    """Respuesta genérica con mensaje informativo."""

    message: str
