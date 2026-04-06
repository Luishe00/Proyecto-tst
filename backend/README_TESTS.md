# README_TESTS

## Objetivo

Este documento resume la estrategia de calidad del backend, cómo ejecutar la suite y qué cobertura protege.

Estado actual validado:

- 70 tests en total
- 70 tests passing
- 95% de cobertura global

## Enfoque de QA

La suite combina caja negra y caja blanca para reducir riesgo funcional y técnico.

- Caja negra:
- CRUD de coches con equivalencia y fronteras en `precio`, `cv`, `peso`, `velocidad_max` y `year`.
- Favoritos con tabla de decisión: autenticado/anónimo, favorito duplicado, coche inexistente.
- Validaciones HTTP de formularios y query params (tipos inválidos, campos obligatorios faltantes, rangos).

- Caja blanca:
- Ramas `if/else` de use cases (`AuthUseCases`, `CarUseCases`, `FavoriteUseCases`).
- Ramas `try/except` en dependencias de seguridad y adaptador de Cloudinary.
- Cobertura de guards de seguridad: usuario ausente, usuario inactivo, rol no admin.

## Arquitectura de tests

Todos los tests viven en `backend/tests`.

Piezas principales:

- `tests/conftest.py`: fixtures compartidos, app de test y aislamiento por función.
- `tests/test_api_*`: integración HTTP (FastAPI + auth + RBAC + validaciones).
- `tests/test_use_cases_*`: lógica de negocio sin red ni base de datos.
- `tests/test_repositories.py`: edge cases de repositorios en memoria.
- `tests/test_car_schemas_validation.py`: validaciones Pydantic de esquemas.
- `tests/test_container.py`: wiring del contenedor y estabilidad de singletons.

## Aislamiento y determinismo

La suite está diseñada para ser repetible y sin dependencia externa:

- Fixtures con `scope="function"` para estado limpio por test.
- Repositorios en memoria efímeros por prueba.
- Mock de subida de imagen para ejecutar offline.
- Tokens de usuario/admin obtenidos por flujo real de login en tests de integración.

## Mocking de Cloudinary

Se intercepta `CloudinaryAdapter.upload_image` con `unittest.mock.patch`.

URL mock estable usada por la suite:

```text
https://res.cloudinary.com/test/image.jpg
```

También se validan ramas de consulta de recurso:

- Recurso existente: devuelve URL.
- `NotFound`: devuelve `None`.

## Comandos de ejecución

Desde la carpeta `backend` y con el entorno activo:

```bash
pytest
```

Con cobertura detallada:

```bash
pytest --cov=. --cov-config=.coveragerc --cov-report=term-missing --cov-report=xml
```

Solo tests de integración API:

```bash
pytest tests/test_api_cars_integration.py tests/test_api_favorites_integration.py tests/test_api_auth_integration.py
```

Solo validaciones y bordes de dominio/esquemas:

```bash
pytest tests/test_car_schemas_validation.py tests/test_repositories.py
```

## Qué riesgos cubre esta suite

- Regresiones de permisos (`admin`, `user`, anónimo).
- Errores de validación de entrada en API (tipos, rangos, campos obligatorios).
- Estados inválidos en favoritos (duplicados, inexistentes).
- Errores de filtrado en catálogo.
- Comportamientos frontera en repositorios en memoria.
- Integración de autenticación JWT y dependencias de seguridad.

## Criterio de calidad recomendado

- Mantener cobertura global >=95%.
- Añadir al menos un test por cada bug corregido.
- En endpoints nuevos, incluir siempre:
- caso feliz
- caso de validación
- caso de autorización
