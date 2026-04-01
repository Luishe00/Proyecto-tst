# 🏎️ Premium Car Catalog — Backend API

API REST profesional desarrollada con **FastAPI** para gestionar un catálogo de coches de alta gama. Diseñada siguiendo **Arquitectura Hexagonal**, principios **SOLID** y **PEP 8**, preparada para pruebas de testing automatizado.

---

## Tabla de Contenidos

1. [Características](#características)
2. [Arquitectura Hexagonal](#arquitectura-hexagonal)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Configuración del Entorno](#configuración-del-entorno)
   - [Opción A — Virtualenv (venv)](#opción-a--virtualenv-venv)
   - [Opción B — Anaconda / Miniconda](#opción-b--anaconda--miniconda)
5. [Ejecución](#ejecución)
6. [Credenciales de Prueba](#credenciales-de-prueba)
7. [Endpoints y Ejemplos de Uso](#endpoints-y-ejemplos-de-uso)
8. [Niveles de Acceso](#niveles-de-acceso)
9. [Filtros Disponibles](#filtros-disponibles)

---

## Características

- ✅ **Arquitectura Hexagonal** (Ports & Adapters)
- ✅ **Autenticación OAuth2 con JWT** (roles: `admin`, `user`, anónimo)
- ✅ **Persistencia In-Memory** (sin base de datos externa, 100% portable)
- ✅ **25 coches premium precargados** (Porsche, Ferrari, Lamborghini, Aston Martin, McLaren)
- ✅ **Validación con Pydantic v2**
- ✅ **Filtrado dinámico** del catálogo por marca, CV, velocidad y precio
- ✅ **Sistema de Favoritos** por usuario
- ✅ **Swagger UI** interactivo en `/docs`
- ✅ **Type Hinting** en todo el proyecto

---

## Arquitectura Hexagonal

El proyecto aplica el patrón **Ports & Adapters** dividiendo el código en tres capas bien definidas:

```
┌─────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE                        │
│   ┌──────────────┐  ┌──────────┐  ┌──────────────────┐  │
│   │  API (FastAPI)│  │  Auth    │  │  Persistence     │  │
│   │  Routers     │  │  JWT     │  │  In-Memory Repos │  │
│   └──────┬───────┘  └────┬─────┘  └────────┬─────────┘  │
│          │               │                  │            │
│   ┌──────▼───────────────▼──────────────────▼─────────┐  │
│   │                   APPLICATION                      │  │
│   │            Casos de Uso (Use Cases)                │  │
│   └──────────────────────┬─────────────────────────────┘  │
│                          │                               │
│   ┌──────────────────────▼─────────────────────────────┐  │
│   │                     DOMAIN                         │  │
│   │         Entidades · Puertos (Interfaces)            │  │
│   └────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

| Capa | Carpeta | Responsabilidad |
|------|---------|-----------------|
| **Domain** | `domain/` | Entidades del negocio (`Car`, `User`, `Favorite`) e interfaces abstractas (puertos) |
| **Application** | `application/` | Lógica de negocio pura: casos de uso que orquestan entidades y puertos |
| **Infrastructure** | `infrastructure/` | Adaptadores concretos: FastAPI, JWT, repositorios en memoria |

**Regla de dependencia:** Las capas internas no conocen las externas. El dominio no importa nada de application ni infrastructure. Los casos de uso solo dependen de los puertos (interfaces), nunca de implementaciones concretas.

---

## Estructura del Proyecto

```
backend/
├── main.py                          # Punto de entrada (uvicorn)
├── requirements.txt
├── README.md
│
├── domain/                          # Capa de Dominio
│   ├── entities/
│   │   ├── car.py                   # Entidad: Coche
│   │   ├── user.py                  # Entidad: Usuario + Enum Role
│   │   └── favorite.py              # Entidad: Favorito
│   └── ports/
│       ├── car_repository.py        # Puerto: interfaz CarRepository
│       ├── user_repository.py       # Puerto: interfaz UserRepository
│       └── favorite_repository.py   # Puerto: interfaz FavoriteRepository
│
├── application/                     # Capa de Aplicación
│   └── use_cases/
│       ├── car_use_cases.py         # CRUD + filtrado de coches
│       ├── auth_use_cases.py        # Autenticación y consulta de usuarios
│       └── favorite_use_cases.py    # Gestión de favoritos
│
└── infrastructure/                  # Capa de Infraestructura
    ├── auth/
    │   └── jwt_handler.py           # Creación/verificación de tokens JWT
    ├── persistence/
    │   ├── seed_data.py             # 25 coches + 2 usuarios precargados
    │   ├── in_memory_car_repository.py
    │   ├── in_memory_user_repository.py
    │   └── in_memory_favorite_repository.py
    └── api/
        ├── main.py                  # App FastAPI + middleware CORS
        ├── container.py             # Contenedor IoC (dependency injection)
        ├── dependencies.py          # Dependencias de seguridad (JWT guards)
        ├── schemas/
        │   ├── car_schemas.py       # CarCreate, CarUpdate, CarFullResponse...
        │   ├── auth_schemas.py      # TokenResponse, UserInfoResponse
        │   └── favorite_schemas.py  # FavoriteResponse, MessageResponse
        └── routers/
            ├── auth.py              # POST /auth/login, GET /auth/me
            ├── cars.py              # CRUD /cars
            └── favorites.py         # CRUD /me/favorites
```

---

## Configuración del Entorno

### Opción A — Virtualenv (venv)

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/premium-car-catalog.git
cd premium-car-catalog/backend

# 2. Crear y activar el entorno virtual
python -m venv venv

# En Windows:
venv\Scripts\activate

# En macOS / Linux:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

### Opción B — Anaconda / Miniconda

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/premium-car-catalog.git
cd premium-car-catalog/backend

# 2. Crear el entorno conda
conda create -n premium-cars python=3.11 -y

# 3. Activar el entorno
conda activate premium-cars

# 4. Instalar dependencias 
pip install -r requirements.txt
```

---

## Ejecución

Desde la carpeta `backend/` con el entorno activo:

```bash
# Opción 1 — Usando el script de entrada
python main.py

# Opción 2 — Directamente con Uvicorn (recomendado para desarrollo)
uvicorn infrastructure.api.main:app --reload --host 0.0.0.0 --port 8000

# Opción 3 — Puerto personalizado
uvicorn infrastructure.api.main:app --reload --port 3000
```

La API estará disponible en:
- **API Base:** `http://localhost:8000`
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## Credenciales de Prueba

| Rol | Usuario | Contraseña | Permisos |
|-----|---------|------------|---------|
| **Admin** | `admin` | `Admin1234!` | CRUD completo del catálogo |
| **Usuario** | `user` | `User1234!` | Lectura + gestión de favoritos |

Para autenticarse, usar el endpoint `POST /auth/login` o el botón **Authorize** de Swagger UI.

---

## Endpoints y Ejemplos de Uso

### Autenticación

```bash
# Login — Obtener token JWT
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=Admin1234!"

# Ver perfil del usuario autenticado
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer <TOKEN>"
```

### Catálogo de Coches

```bash
# Listado público (sin token — devuelve solo marca, modelo, imagen)
curl "http://localhost:8000/cars"

# Listado completo (con token)
curl "http://localhost:8000/cars" \
  -H "Authorization: Bearer <TOKEN>"

# Detalle de un coche (requiere autenticación)
curl "http://localhost:8000/cars/1" \
  -H "Authorization: Bearer <TOKEN>"

# Crear coche (requiere Admin)
curl -X POST "http://localhost:8000/cars" \
  -H "Authorization: Bearer <TOKEN_ADMIN>" \
  -H "Content-Type: application/json" \
  -d '{"marca":"Bugatti","modelo":"Chiron","cv":1500,"peso":1995,"velocidad_max":420,"precio":3200000,"imagen_url":"https://example.com/chiron.jpg"}'

# Actualizar coche (requiere Admin)
curl -X PUT "http://localhost:8000/cars/1" \
  -H "Authorization: Bearer <TOKEN_ADMIN>" \
  -H "Content-Type: application/json" \
  -d '{"precio":250000}'

# Eliminar coche (requiere Admin)
curl -X DELETE "http://localhost:8000/cars/1" \
  -H "Authorization: Bearer <TOKEN_ADMIN>"
```

### Favoritos

```bash
# Ver mis favoritos
curl "http://localhost:8000/me/favorites" \
  -H "Authorization: Bearer <TOKEN>"

# Añadir coche a favoritos
curl -X POST "http://localhost:8000/me/favorites/6" \
  -H "Authorization: Bearer <TOKEN>"

# Eliminar coche de favoritos
curl -X DELETE "http://localhost:8000/me/favorites/6" \
  -H "Authorization: Bearer <TOKEN>"
```

---

## Niveles de Acceso

| Endpoint | Anónimo | Usuario | Admin |
|----------|---------|---------|-------|
| `GET /cars` | ✅ (limitado) | ✅ (completo) | ✅ |
| `GET /cars/{id}` | ❌ | ✅ | ✅ |
| `POST /cars` | ❌ | ❌ | ✅ |
| `PUT /cars/{id}` | ❌ | ❌ | ✅ |
| `DELETE /cars/{id}` | ❌ | ❌ | ✅ |
| `GET /me/favorites` | ❌ | ✅ | ✅ |
| `POST /me/favorites/{id}` | ❌ | ✅ | ✅ |
| `DELETE /me/favorites/{id}` | ❌ | ✅ | ✅ |

---

## Filtros Disponibles

El endpoint `GET /cars` admite los siguientes parámetros de consulta:

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `marca` | `string` | Marca exacta del coche (insensible a mayúsculas) | `?marca=Porsche` |
| `velocidad_max` | `integer` | Velocidad máxima mínima en km/h | `?velocidad_max=350` |
| `cv` | `integer` | Caballos de vapor mínimos | `?cv=700` |
| `precio_min` | `float` | Precio mínimo en euros | `?precio_min=100000` |
| `precio_max` | `float` | Precio máximo en euros | `?precio_max=500000` |

### Ejemplos de URL con filtros

```
# Todos los Ferrari
GET /cars?marca=Ferrari

# Coches con más de 800 CV
GET /cars?cv=800

# Coches con velocidad máxima de al menos 350 km/h
GET /cars?velocidad_max=350

# Coches entre 200.000 € y 500.000 €
GET /cars?precio_min=200000&precio_max=500000

# Porsche con más de 600 CV y precio máximo de 500.000 €
GET /cars?marca=Porsche&cv=600&precio_max=500000

# McLaren con velocidad ≥ 340 km/h
GET /cars?marca=McLaren&velocidad_max=340
```

---

## Tecnologías Utilizadas

| Tecnología | Versión | Uso |
|------------|---------|-----|
| Python | 3.11+ | Lenguaje base |
| FastAPI | 0.111 | Framework web |
| Pydantic | v2 | Validación de datos |
| python-jose | 3.3 | Tokens JWT |
| passlib + bcrypt | 1.7 | Hash de contraseñas |
| Uvicorn | 0.29 | Servidor ASGI |

---

*Proyecto preparado para testing. Arquitectura limpia, sin dependencias externas de base de datos.*
