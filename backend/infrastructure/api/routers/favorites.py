"""
Router de favoritos de usuario.
Permite a los usuarios autenticados gestionar su lista personal de coches favoritos.
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from application.use_cases.favorite_use_cases import FavoriteUseCases
from domain.entities.user import User
from infrastructure.api.container import get_favorite_use_cases
from infrastructure.api.dependencies import get_current_user
from infrastructure.api.schemas.car_schemas import CarFullResponse
from infrastructure.api.schemas.favorite_schemas import FavoriteResponse, MessageResponse

router = APIRouter(prefix="/me/favorites", tags=["Mis Favoritos"])


@router.get(
    "",
    response_model=List[CarFullResponse],
    summary="Ver mis coches favoritos",
    description="Devuelve la lista completa de coches en favoritos del usuario autenticado.",
)
async def get_favorites(
    current_user: User = Depends(get_current_user),
    use_cases: FavoriteUseCases = Depends(get_favorite_use_cases),
) -> List[CarFullResponse]:
    cars = use_cases.get_favorites(current_user.id)
    return [CarFullResponse.model_validate(car.model_dump()) for car in cars]


@router.post(
    "/{car_id}",
    response_model=FavoriteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Añadir coche a favoritos",
    description="Añade el coche indicado a la lista de favoritos del usuario autenticado.",
)
async def add_favorite(
    car_id: int,
    current_user: User = Depends(get_current_user),
    use_cases: FavoriteUseCases = Depends(get_favorite_use_cases),
) -> FavoriteResponse:
    try:
        favorite = use_cases.add_favorite(current_user.id, car_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    return FavoriteResponse.model_validate(favorite.model_dump())


@router.delete(
    "/{car_id}",
    response_model=MessageResponse,
    summary="Eliminar coche de favoritos",
    description="Elimina el coche indicado de la lista de favoritos del usuario autenticado.",
)
async def remove_favorite(
    car_id: int,
    current_user: User = Depends(get_current_user),
    use_cases: FavoriteUseCases = Depends(get_favorite_use_cases),
) -> MessageResponse:
    try:
        use_cases.remove_favorite(current_user.id, car_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    return MessageResponse(message=f"Coche con ID {car_id} eliminado de tus favoritos.")
