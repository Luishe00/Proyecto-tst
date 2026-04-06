"""
Router del catálogo de coches.
Expone endpoints CRUD con distintos niveles de acceso según el rol del usuario.
"""
from typing import Annotated, List, Optional, Union

from fastapi import APIRouter, Depends, Form, HTTPException, Query, UploadFile, status

from application.use_cases.car_use_cases import CarUseCases
from domain.entities.user import User
from infrastructure.api.container import get_car_use_cases
from infrastructure.api.dependencies import get_admin_user, get_current_user, get_optional_current_user
from infrastructure.api.schemas.car_schemas import (
    CarFullResponse,
    CarPublicResponse,
    CarUpdate,
)
from infrastructure.api.schemas.favorite_schemas import MessageResponse

router = APIRouter(prefix="/cars", tags=["Catálogo de Coches"])


@router.get(
    "",
    summary="Listar catálogo de coches",
    description=(
        "Devuelve el catálogo completo con filtros opcionales.\n\n"
        "- **Anónimo**: solo recibe `id`, `marca`, `modelo` e `imagen_url`.\n"
        "- **Usuario autenticado**: recibe la ficha técnica completa.\n\n"
        "**Parámetros de filtro:**\n"
        "- `marca`: filtra por nombre exacto de marca (ej: `Porsche`).\n"
        "- `velocidad_max`: muestra coches con velocidad máxima **≥** al valor.\n"
        "- `cv`: muestra coches con potencia **≥** al valor indicado.\n"
        "- `precio_min` / `precio_max`: rango de precio en euros.\n"
        "- `year`: filtra por año de fabricación exacto.\n"
        "- `year_min`: muestra coches fabricados desde ese año en adelante."
    ),
)
async def get_cars(
    marca: Annotated[Optional[str], Query(description="Filtrar por marca (ej: Ferrari)")] = None,
    velocidad_max: Annotated[Optional[int], Query(description="Velocidad máxima mínima en km/h", ge=1)] = None,
    cv: Annotated[Optional[int], Query(description="Caballos de vapor mínimos", ge=1)] = None,
    precio_min: Annotated[Optional[float], Query(description="Precio mínimo en euros", ge=0)] = None,
    precio_max: Annotated[Optional[float], Query(description="Precio máximo en euros", ge=0)] = None,
    year: Annotated[Optional[int], Query(description="Año de fabricación exacto", gt=1885, le=2027)] = None,
    year_min: Annotated[Optional[int], Query(description="Año mínimo de fabricación", gt=1885, le=2027)] = None,
    current_user: Optional[User] = Depends(get_optional_current_user),
    use_cases: CarUseCases = Depends(get_car_use_cases),
) -> List[Union[CarFullResponse, CarPublicResponse]]:
    cars = use_cases.get_all_cars(
        marca=marca,
        velocidad_max=velocidad_max,
        cv=cv,
        precio_min=precio_min,
        precio_max=precio_max,
        year=year,
        year_min=year_min,
    )
    if current_user:
        return [CarFullResponse.model_validate(car.model_dump()) for car in cars]
    return [CarPublicResponse.model_validate(car.model_dump()) for car in cars]


@router.get(
    "/{car_id}",
    response_model=CarFullResponse,
    summary="Obtener ficha técnica de un coche",
    description="Devuelve la ficha técnica completa de un coche por su ID. Requiere autenticación.",
)
async def get_car(
    car_id: int,
    current_user: User = Depends(get_current_user),
    use_cases: CarUseCases = Depends(get_car_use_cases),
) -> CarFullResponse:
    car = use_cases.get_car_by_id(car_id)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coche con ID {car_id} no encontrado en el catálogo.",
        )
    return CarFullResponse.model_validate(car.model_dump())


@router.post(
    "",
    response_model=CarFullResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Añadir un coche al catálogo",
    description="Crea un nuevo coche en el catálogo. Acepta `multipart/form-data` con campos del coche e imagen opcional. **Requiere rol Admin.**",
)
async def create_car(
    marca: Annotated[str, Form(min_length=2, max_length=50, description="Marca del fabricante")],
    modelo: Annotated[str, Form(min_length=1, max_length=100, description="Nombre del modelo")],
    cv: Annotated[int, Form(gt=0, le=2000, description="Potencia en caballos de vapor")],
    peso: Annotated[int, Form(gt=0, le=5000, description="Peso en kg")],
    velocidad_max: Annotated[int, Form(gt=0, le=500, description="Velocidad máxima en km/h")],
    precio: Annotated[float, Form(gt=0, description="Precio en euros")],
    year: Annotated[int, Form(gt=1885, le=2027, description="Año de fabricación")],
    imagen_url: Annotated[Optional[str], Form(description="URL de la imagen (si no se sube archivo)")] = None,
    imagen: Optional[UploadFile] = None,
    _admin: User = Depends(get_admin_user),
    use_cases: CarUseCases = Depends(get_car_use_cases),
) -> CarFullResponse:
    car_data = {
        "marca": marca,
        "modelo": modelo,
        "cv": cv,
        "peso": peso,
        "velocidad_max": velocidad_max,
        "precio": precio,
        "year": year,
        "imagen_url": imagen_url or "",
    }

    image_file: Optional[bytes] = None
    image_filename: Optional[str] = None
    if imagen and imagen.filename:
        image_file = await imagen.read()
        image_filename = f"{marca.lower().replace(' ', '_')}_{modelo.lower().replace(' ', '_')}"

    if not image_file and not imagen_url:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Debes proporcionar una imagen (archivo) o una imagen_url.",
        )

    new_car = use_cases.create_car(car_data, image_file=image_file, image_filename=image_filename)
    return CarFullResponse.model_validate(new_car.model_dump())


@router.put(
    "/{car_id}",
    response_model=CarFullResponse,
    summary="Actualizar un coche",
    description="Actualiza los datos de un coche existente. **Requiere rol Admin.**",
)
async def update_car(
    car_id: int,
    car_data: CarUpdate,
    _admin: User = Depends(get_admin_user),
    use_cases: CarUseCases = Depends(get_car_use_cases),
) -> CarFullResponse:
    updated_car = use_cases.update_car(car_id, car_data.model_dump())
    if not updated_car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coche con ID {car_id} no encontrado en el catálogo.",
        )
    return CarFullResponse.model_validate(updated_car.model_dump())


@router.delete(
    "/{car_id}",
    response_model=MessageResponse,
    summary="Eliminar un coche del catálogo",
    description="Elimina un coche del catálogo de forma permanente. **Requiere rol Admin.**",
)
async def delete_car(
    car_id: int,
    _admin: User = Depends(get_admin_user),
    use_cases: CarUseCases = Depends(get_car_use_cases),
) -> MessageResponse:
    deleted = use_cases.delete_car(car_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coche con ID {car_id} no encontrado en el catálogo.",
        )
    return MessageResponse(message=f"Coche con ID {car_id} eliminado correctamente del catálogo.")
