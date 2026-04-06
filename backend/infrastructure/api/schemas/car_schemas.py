"""
Esquemas Pydantic para los endpoints de coches.
Define los modelos de request/response para la API REST.
"""
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class CarPublicResponse(BaseModel):
    """
    Respuesta pública del coche para usuarios no autenticados.
    Solo expone la información básica: marca, modelo e imagen.
    """

    id: int
    marca: str
    modelo: str
    imagen_url: str

    model_config = {"from_attributes": True}


class CarFullResponse(BaseModel):
    """
    Ficha técnica completa del coche para usuarios autenticados.
    Incluye todos los datos técnicos y económicos del vehículo.
    """

    id: int
    marca: str
    modelo: str
    cv: int = Field(..., description="Caballos de vapor")
    peso: int = Field(..., description="Peso en kg")
    velocidad_max: int = Field(..., description="Velocidad máxima en km/h")
    precio: float = Field(..., description="Precio en euros")
    imagen_url: str
    year: int = Field(..., gt=1885, le=2027, description="Año de fabricación")

    @field_validator("year")
    @classmethod
    def year_not_future(cls, v: int) -> int:
        max_year = date.today().year + 1
        if v > max_year:
            raise ValueError(f"El año no puede ser superior a {max_year}")
        return v

    model_config = {"from_attributes": True}


class CarCreate(BaseModel):
    """Esquema de entrada para crear un nuevo coche en el catálogo (solo Admin)."""

    marca: str = Field(..., min_length=2, max_length=50, description="Marca del fabricante", examples=["Ferrari"])
    modelo: str = Field(..., min_length=1, max_length=100, description="Nombre del modelo", examples=["SF90 Stradale"])
    cv: int = Field(..., gt=0, le=2000, description="Potencia en caballos de vapor", examples=[1000])
    peso: int = Field(..., gt=0, le=5000, description="Peso del vehículo en kg", examples=[1570])
    velocidad_max: int = Field(..., gt=0, le=500, description="Velocidad máxima en km/h", examples=[340])
    precio: float = Field(..., gt=0, description="Precio en euros", examples=[507000])
    imagen_url: str = Field(..., description="URL de la imagen del coche", examples=["https://example.com/car.jpg"])
    year: int = Field(..., gt=1885, le=2027, description="Año de fabricación", examples=[2022])

    @field_validator("year")
    @classmethod
    def year_not_future(cls, v: int) -> int:
        max_year = date.today().year + 1
        if v > max_year:
            raise ValueError(f"El año no puede ser superior a {max_year}")
        return v


class CarUpdate(BaseModel):
    """Esquema de entrada para actualizar un coche existente (solo Admin). Todos los campos son opcionales."""

    marca: Optional[str] = Field(default=None, min_length=2, max_length=50)
    modelo: Optional[str] = Field(default=None, min_length=1, max_length=100)
    cv: Optional[int] = Field(default=None, gt=0, le=2000)
    peso: Optional[int] = Field(default=None, gt=0, le=5000)
    velocidad_max: Optional[int] = Field(default=None, gt=0, le=500)
    precio: Optional[float] = Field(default=None, gt=0)
    imagen_url: Optional[str] = Field(default=None)
    year: Optional[int] = Field(default=None, gt=1885, le=2027, description="Año de fabricación")

    @field_validator("year")
    @classmethod
    def year_not_future(cls, v: Optional[int]) -> Optional[int]:
        if v is None:
            return v
        max_year = date.today().year + 1
        if v > max_year:
            raise ValueError(f"El año no puede ser superior a {max_year}")
        return v
