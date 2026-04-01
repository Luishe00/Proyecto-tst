"""
Router de autenticación.
Expone el endpoint de login OAuth2 con JWT.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from application.use_cases.auth_use_cases import AuthUseCases
from domain.entities.user import User
from infrastructure.api.container import get_auth_use_cases, get_jwt_handler
from infrastructure.api.dependencies import get_current_user
from infrastructure.api.schemas.auth_schemas import TokenResponse, UserInfoResponse
from infrastructure.auth.jwt_handler import JWTHandler

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Iniciar sesión",
    description=(
        "Autentica al usuario con nombre de usuario y contraseña. "
        "Devuelve un token JWT Bearer que debe incluirse en el header "
        "`Authorization: Bearer <token>` para acceder a los recursos protegidos.\n\n"
        "**Credenciales de prueba:**\n"
        "- Admin: `admin` / `Admin1234!`\n"
        "- Usuario: `user` / `User1234!`"
    ),
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_uc: AuthUseCases = Depends(get_auth_use_cases),
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
) -> TokenResponse:
    user = auth_uc.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de usuario o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = jwt_handler.create_access_token(
        data={"sub": user.username, "role": user.role.value, "user_id": user.id}
    )
    return TokenResponse(access_token=token)


@router.get(
    "/me",
    response_model=UserInfoResponse,
    summary="Obtener información del usuario actual",
    description="Devuelve la información del usuario autenticado. Requiere token JWT válido.",
)
async def get_me(current_user: User = Depends(get_current_user)) -> UserInfoResponse:
    return UserInfoResponse(
        id=current_user.id,
        username=current_user.username,
        role=current_user.role.value,
    )
