"""
Entidad de dominio: Coche.
Representa un coche premium en el catálogo.
"""
from pydantic import BaseModel, Field


class Car(BaseModel):
    """Entidad principal del dominio que representa un coche premium."""

    id: int = Field(default=0, description="Identificador único del coche")
    marca: str = Field(..., min_length=2, max_length=50, description="Marca del fabricante")
    modelo: str = Field(..., min_length=1, max_length=100, description="Nombre del modelo")
    cv: int = Field(..., gt=0, le=2000, description="Potencia en caballos de vapor")
    peso: int = Field(..., gt=0, le=5000, description="Peso del vehículo en kilogramos")
    velocidad_max: int = Field(..., gt=0, le=500, description="Velocidad máxima en km/h")
    precio: float = Field(..., gt=0, description="Precio en euros")
    imagen_url: str = Field(..., description="URL de la imagen del coche")

    model_config = {"from_attributes": True}
