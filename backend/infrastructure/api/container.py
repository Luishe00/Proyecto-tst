"""
Contenedor de dependencias (IoC Container).
Instancia los repositorios, casos de uso y servicios como singletons
e inyecta el seed data al arrancar la aplicación.
"""
from application.use_cases.auth_use_cases import AuthUseCases
from application.use_cases.car_use_cases import CarUseCases
from application.use_cases.favorite_use_cases import FavoriteUseCases
from infrastructure.adapters.cloudinary_adapter import CloudinaryAdapter
from infrastructure.auth.jwt_handler import JWTHandler
from infrastructure.persistence.in_memory_car_repository import InMemoryCarRepository
from infrastructure.persistence.in_memory_favorite_repository import InMemoryFavoriteRepository
from infrastructure.persistence.in_memory_user_repository import InMemoryUserRepository
from infrastructure.persistence.seed_data import SEED_CARS, SEED_USERS

# ── Singletons de repositorios ───────────────────────────────────────────────
_car_repository = InMemoryCarRepository()
_user_repository = InMemoryUserRepository()
_favorite_repository = InMemoryFavoriteRepository()
_jwt_handler = JWTHandler()
_cloudinary_adapter = CloudinaryAdapter()

# ── Carga del seed data al iniciar ───────────────────────────────────────────
for _car in SEED_CARS:
    _car_repository.create(_car)

for _user in SEED_USERS:
    _user_repository.create(_user)


# ── Funciones de fábrica para FastAPI Depends() ──────────────────────────────

def get_car_use_cases() -> CarUseCases:
    """Devuelve la instancia singleton de CarUseCases."""
    return CarUseCases(repository=_car_repository, image_storage=_cloudinary_adapter)


def get_car_repository() -> InMemoryCarRepository:
    """Devuelve el repositorio de coches (usado para la migración de imágenes)."""
    return _car_repository


def get_auth_use_cases() -> AuthUseCases:
    """Devuelve la instancia singleton de AuthUseCases."""
    return AuthUseCases(repository=_user_repository)


def get_favorite_use_cases() -> FavoriteUseCases:
    """Devuelve la instancia singleton de FavoriteUseCases."""
    return FavoriteUseCases(
        favorite_repository=_favorite_repository,
        car_repository=_car_repository,
    )


def get_jwt_handler() -> JWTHandler:
    """Devuelve la instancia singleton de JWTHandler."""
    return _jwt_handler
