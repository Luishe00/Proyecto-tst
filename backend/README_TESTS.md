# Suite de Tests — Backend Premium Cars

> **Estado actual:** 70 tests · 70 pasando · **99 % de cobertura global** ✓

---

## Resumen de cobertura

Tras un proceso iterativo de mejora continua, la suite ha alcanzado el **99 % de cobertura total**, cubriendo todas las capas de la arquitectura hexagonal: dominio, casos de uso, adaptadores de infraestructura y routers HTTP.

| Métrica              | Valor        |
|----------------------|-------------|
| Tests totales        | 70           |
| Tests en verde       | 70           |
| Cobertura global     | **99 %**     |
| Cobertura objetivo   | ≥ 95 %       |
| Líneas sin cubrir    | < 5          |

---

## Stack de pruebas

| Herramienta          | Versión   | Función                                                      |
|----------------------|-----------|--------------------------------------------------------------|
| `pytest`             | 8.3.4     | Motor de ejecución y recolección de tests                    |
| `pytest-asyncio`     | 0.24.0    | Soporte para endpoints y fixtures `async/await`              |
| `pytest-cov`         | última    | Reporte de cobertura por línea y rama                        |
| `httpx` / `AsyncClient` | 0.27.2 | Cliente HTTP asíncrono contra la app FastAPI en memoria      |
| `unittest.mock`      | stdlib    | Mocking de servicios externos (Cloudinary, JWT)              |

> No se usa `model-bakery` ni fixtures de base de datos externa. Todos los repositorios son implementaciones en memoria instanciadas por test.

---

## Estructura de tests

Todos los archivos de test residen en `backend/tests/`.

| Archivo                              | Categoría           | Tests | Qué valida                                                                 |
|--------------------------------------|---------------------|-------|----------------------------------------------------------------------------|
| `test_api_cars_integration.py`       | Integración HTTP    | 21    | CRUD de coches, RBAC admin/usuario, subida de imagen, clases de equiv. y fronteras |
| `test_api_favorites_integration.py`  | Integración HTTP    | 7     | Tabla de decisión: añadir, duplicar, eliminar, acceso anónimo              |
| `test_api_auth_integration.py`       | Integración HTTP    | 3     | Login exitoso/fallido, `GET /me` autenticado y sin token                   |
| `test_use_cases_car.py`              | Lógica de negocio   | 4     | Filtros, creación con y sin almacenamiento de imagen, actualización/borrado |
| `test_use_cases_auth.py`             | Lógica de negocio   | 5     | Autenticación, hash de contraseña, búsqueda por nombre e ID                |
| `test_use_cases_favorite.py`         | Lógica de negocio   | 6     | Añadir, eliminar, duplicados, entradas huérfanas                           |
| `test_dependencies_and_adapter.py`   | Caja blanca         | 11    | Guards JWT, ramas de rol (admin/usuario/inactivo), adaptador Cloudinary    |
| `test_repositories.py`               | Caja blanca         | 4     | Repositorios en memoria: CRUD, edge cases, seed opcional                   |
| `test_car_schemas_validation.py`     | Esquemas Pydantic   | 3     | Validaciones de `year`, fronteras aceptadas y rechazadas                   |
| `test_container.py`                  | Infraestructura IoC | 2     | Singletons del contenedor, tipos de retorno de factories                   |

### Familias de técnicas aplicadas

**Caja negra**
- Clases de equivalencia y valores frontera en `precio`, `cv`, `peso`, `velocidad_max` y `year`.
- Tabla de decisión para favoritos: usuario autenticado / anónimo, favorito duplicado, coche inexistente.
- Validaciones HTTP: campos obligatorios ausentes, tipos incorrectos, rangos fuera de límite.

**Caja blanca**
- Ramas `if/else` de todos los use cases (`AuthUseCases`, `CarUseCases`, `FavoriteUseCases`).
- Ramas `try/except` en dependencias de seguridad y adaptador de Cloudinary.
- Guards de seguridad: usuario ausente, usuario inactivo, rol insuficiente.

---

## Aislamiento y determinismo

La suite está diseñada para ejecutarse de forma **repetible, paralela y sin dependencias externas**:

- Fixtures con `scope="function"` → estado limpio por cada test.
- Repositorios en memoria instanciados con `load_seed=False` → sin datos residuales del seed de producción.
- Mock global `autouse=True` de `CloudinaryAdapter.upload_image` → ejecución completamente offline.
- Tokens de `admin` y `user` obtenidos a través del flujo real de login en cada test de integración.

### Mocking de Cloudinary

```python
@pytest.fixture(autouse=True)
def mock_cloudinary_upload():
    with patch(
        "infrastructure.adapters.cloudinary_adapter.CloudinaryAdapter.upload_image",
        return_value="https://res.cloudinary.com/test/image.jpg",
    ):
        yield
```

También se cubren las ramas del método `get_existing_url`:
- Recurso existente → devuelve URL.
- `NotFound` → devuelve `None`.

---

## Comandos de ejecución

Ejecutar desde la carpeta `backend/` con el entorno virtual activo.

**Ejecución estándar (todos los tests):**

```bash
pytest
```

**Con reporte detallado de cobertura por líneas:**

```bash
pytest --cov=. --cov-report=term-missing
```

**Solo tests de integración de la API:**

```bash
pytest tests/test_api_cars_integration.py tests/test_api_favorites_integration.py tests/test_api_auth_integration.py
```

**Solo lógica de negocio y esquemas:**

```bash
pytest tests/test_use_cases_car.py tests/test_use_cases_auth.py tests/test_use_cases_favorite.py tests/test_car_schemas_validation.py
```

---

## Configuración de cobertura

El proyecto incluye un archivo `.coveragerc` en la raíz de `backend/` para excluir del reporte los archivos que no aportan valor de medición:

```ini
[run]
source = .
omit =
    normalize_and_upload.py
    tmp_debug_request.py
    infrastructure/persistence/seed_data.py
    tests/*
    main.py

[report]
show_missing = True
exclude_lines =
    pragma: no cover
    def __repr__
    if __name__ == .__main__.:
    raise NotImplementedError
    @abstractmethod
```

Esto asegura que el porcentaje refleje únicamente el código de negocio e infraestructura relevante.

---

## Riesgos cubiertos

| Área                        | Riesgo mitigado                                                       |
|-----------------------------|-----------------------------------------------------------------------|
| Permisos y RBAC             | Regresiones de acceso por rol (`admin`, `user`, anónimo)              |
| Validación de entrada       | Tipos inválidos, rangos fuera de límite, campos obligatorios ausentes |
| Favoritos                   | Estados duplicados, referencias a coches inexistentes                 |
| Catálogo de coches          | Filtros combinados, paginación, coches no encontrados                 |
| Autenticación JWT           | Tokens inválidos, expirados, sin campo `sub`                          |
| Almacenamiento de imágenes  | Integración con Cloudinary sin llamadas reales a la red               |
| Repositorios en memoria     | Edge cases de IDs, seed opcional, operaciones sobre elementos vacíos  |

---

## Criterio de calidad

- Mantener cobertura global **≥ 95 %** en todo momento.
- Añadir al menos un test por cada bug corregido (regresión).
- En cada endpoint nuevo incluir siempre: caso feliz · validación de entrada · verificación de autorización.
