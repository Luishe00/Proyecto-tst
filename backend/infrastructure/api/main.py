"""
Punto de entrada principal de la aplicación FastAPI.
Configura la app, middleware CORS e incluye todos los routers.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.api.routers import auth, cars, favorites
from infrastructure.api.container import get_car_repository

# ---------------------------------------------------------------------------
# Instancia de la aplicación FastAPI con metadata para Swagger UI
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Premium Car Catalog API",
    description="""
## 🏎️ API de Catálogo de Coches Premium

API REST profesional para gestionar un catálogo de vehículos de alta gama.

---

### Niveles de Acceso

| Rol | Descripción | Permisos |
|-----|-------------|----------|
| **Anónimo** | Sin token JWT | `GET /cars` (solo marca, modelo e imagen) |
| **Usuario** | Token JWT con rol `user` | Ficha técnica completa + gestión de favoritos |
| **Admin** | Token JWT con rol `admin` | CRUD completo del catálogo |

---

### Credenciales de Prueba

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| `admin` | `Admin1234!` | Administrador |
| `user` | `User1234!` | Usuario |

---

### Marcas Disponibles
**Porsche** · **Ferrari** · **Lamborghini** · **Aston Martin** · **McLaren**
    """,
    version="1.0.0",
    contact={
        "name": "Premium Car Catalog",
        "url": "https://github.com/tu-usuario/premium-car-catalog",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=[
        {"name": "Autenticación", "description": "Login con OAuth2 y gestión de sesión."},
        {"name": "Catálogo de Coches", "description": "Consulta y administración del catálogo."},
        {"name": "Mis Favoritos", "description": "Lista personal de coches favoritos."},
        {"name": "Health", "description": "Estado del servicio."},
    ],
)

# ---------------------------------------------------------------------------
# Middleware CORS
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Registro de routers
# ---------------------------------------------------------------------------
app.include_router(auth.router)
app.include_router(cars.router)
app.include_router(favorites.router)


# ---------------------------------------------------------------------------
# Migración de imágenes al arrancar
# ---------------------------------------------------------------------------
@app.on_event("startup")
async def startup_event() -> None:
    """Migra las imágenes del seed a Cloudinary al arrancar la aplicación."""
    import logging
    from infrastructure.persistence.seed_data import migrate_seed_images

    logger = logging.getLogger(__name__)
    try:
        await migrate_seed_images(get_car_repository())
    except Exception as exc:  # noqa: BLE001
        logger.warning("La migración de imágenes a Cloudinary falló: %s", exc)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/", tags=["Health"], summary="Estado del servicio")
async def root() -> dict:
    """Verifica que el servicio esté en funcionamiento."""
    return {
        "service": "Premium Car Catalog API",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs",
    }
