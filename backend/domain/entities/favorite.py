"""
Entidad de dominio: Favorito.
Representa la relación entre un usuario y un coche favorito.
"""
from pydantic import BaseModel, Field


class Favorite(BaseModel):
    """Entidad que representa un coche favorito de un usuario."""

    id: int = Field(default=0, description="Identificador único del favorito")
    user_id: int = Field(..., description="ID del usuario propietario")
    car_id: int = Field(..., description="ID del coche marcado como favorito")

    model_config = {"from_attributes": True}
