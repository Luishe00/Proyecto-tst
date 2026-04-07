"""
Datos de seed para inicializar el sistema con coches premium y usuarios de prueba.
Incluye 20 coches reales (4 por cada marca premium) y 2 usuarios (admin y user).
"""
import asyncio
import logging

import httpx
from passlib.context import CryptContext

from domain.entities.car import Car
from domain.entities.user import Role, User

logger = logging.getLogger(__name__)

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------------------------------------------------------------------------
# 20 Coches Premium con URLs de Cloudinary válidas
# ---------------------------------------------------------------------------
SEED_CARS: list[Car] = [
    Car(
        id=1,
        marca="Aston Martin",
        modelo="DB11 AMR",
        precio=241500.0,
        cv=639,
        peso=1870,
        velocidad_max=334,
        imagen_url="https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501561/premium_cars_catalog/astonmartin-db11amr.jpg",
        year=2022,
    ),
    Car(
        id=2,
        marca="Aston Martin",
        modelo="DBS Superleggera",
        precio=316000.0,
        cv=725,
        peso=1845,
        velocidad_max=340,
        imagen_url="https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501562/premium_cars_catalog/astonmartin-dbs-superleggera.jpg",
        year=2021,
    ),
    Car(
        id=3,
        marca="Aston Martin",
        modelo="Valkyrie",
        precio=3000000.0,
        cv=1160,
        peso=1030,
        velocidad_max=402,
        imagen_url="https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501562/premium_cars_catalog/astonmartin-valkyrie.jpg",
        year=2023,
    ),
    Car(
        id=4,
        marca="Aston Martin",
        modelo="Vantage V12",
        precio=215000.0,
        cv=700,
        peso=1795,
        velocidad_max=322,
        imagen_url="https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501563/premium_cars_catalog/astonmartin-vantage-v12.jpg",
        year=2023,
    ),
    Car(
        id=5,
        marca="Ferrari",
        modelo="F8 Tributo",
        precio=276000.0,
        cv=720,
        peso=1435,
        velocidad_max=340,
        imagen_url="https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501564/premium_cars_catalog/ferrari-f8-tributo.jpg",
        year=2022,
    ),
    Car(
        id=6,
        marca="Ferrari",
        modelo="LaFerrari",
        precio=1800000.0,
        cv=963,
        peso=1585,
        velocidad_max=352,
        imagen_url="https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501564/premium_cars_catalog/ferrari-laferrari.jpg",
        year=2016,
    ),
    Car(
        id=7,
        marca="Ferrari",
        modelo="Roma",
        precio=247171.0,
        cv=620,
        peso=1570,
        velocidad_max=320,
        imagen_url="https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501565/premium_cars_catalog/ferrari-roma.jpg",
        year=2023,
    ),
    Car(
        id=8,
        marca="Ferrari",
        modelo="SF90 Stradale",
        precio=465000.0,
        cv=1000,
        peso=1570,
        velocidad_max=340,
        imagen_url="https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501566/premium_cars_catalog/ferrari-sf90-stradale.jpg",
        year=2023,
    ),
    Car(
        id=9,
        marca="Lamborghini",
        modelo="Huracán EVO",
        precio=259000.0,
        cv=640,
        peso=1422,
        velocidad_max=325,
        imagen_url="https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501566/premium_cars_catalog/lamborghin-hurac%C3%A1n-evo.jpg",
        year=2022,
    ),
    Car(
        id=10,
        marca="Lamborghini",
        modelo="Aventador SVJ",
        precio=445000.0,
        cv=770,
        peso=1525,
        velocidad_max=350,
        imagen_url="https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501567/premium_cars_catalog/lamborghini-aventador-svj.jpg",
        year=2021,
    ),
    Car(
        id=11,
        marca="Lamborghini",
        modelo="Sián FKP 37",
        precio=3600000.0,
        cv=819,
        peso=1595,
        velocidad_max=350,
        imagen_url="https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501569/premium_cars_catalog/lamborghini-si%C3%A1n-fkp-37.jpg",
        year=2021,
    ),
    Car(
        id=12,
        marca="Lamborghini",
        modelo="Urus Performante",
        precio=280000.0,
        cv=666,
        peso=2150,
        velocidad_max=306,
        imagen_url="https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501569/premium_cars_catalog/lamborghini-urus-performante.jpg",
        year=2023,
    ),
    Car(
        id=13,
        marca="McLaren",
        modelo="720S",
        precio=310000.0,
        cv=720,
        peso=1419,
        velocidad_max=341,
        imagen_url="https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501570/premium_cars_catalog/mclaren-720s.jpg",
        year=2021,
    ),
    Car(
        id=14,
        marca="McLaren",
        modelo="Senna",
        precio=965000.0,
        cv=800,
        peso=1198,
        velocidad_max=335,
        imagen_url="https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501571/premium_cars_catalog/mclaren-senna.jpg",
        year=2020,
    ),
    Car(
        id=15,
        marca="McLaren",
        modelo="Speedtail",
        precio=2200000.0,
        cv=1070,
        peso=1430,
        velocidad_max=403,
        imagen_url="https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501572/premium_cars_catalog/mclaren-speedtail.png",
        year=2020,
    ),
    Car(
        id=16,
        marca="Porsche",
        modelo="918 Spyder",
        precio=875000.0,
        cv=887,
        peso=1674,
        velocidad_max=345,
        imagen_url="https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501573/premium_cars_catalog/porsche-918-spyder-2018.jpg",
        year=2018,
    ),
    Car(
        id=17,
        marca="Porsche",
        modelo="Cayenne Turbo GT",
        precio=212000.0,
        cv=659,
        peso=2220,
        velocidad_max=305,
        imagen_url="https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501573/premium_cars_catalog/porsche-cayenne-turbo-gt.jpg",
        year=2023,
    ),
    Car(
        id=18,
        marca="Porsche",
        modelo="Panamera Turbo S",
        precio=217000.0,
        cv=630,
        peso=2070,
        velocidad_max=315,
        imagen_url="https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501574/premium_cars_catalog/porsche-panamera-turbo-s.jpg",
        year=2022,
    ),
    Car(
        id=19,
        marca="Porsche",
        modelo="Taycan Turbo S",
        precio=196000.0,
        cv=761,
        peso=2295,
        velocidad_max=260,
        imagen_url="https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501575/premium_cars_catalog/porsche-taycan-turbo-s.jpg",
        year=2023,
    ),
    Car(
        id=20,
        marca="Porsche",
        modelo="911 GT3 RS",
        precio=265000.0,
        cv=525,
        peso=1450,
        velocidad_max=296,
        imagen_url="https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501576/premium_cars_catalog/porsche911-gt3-rs.jpg",
        year=2024,
    ),
]

# ---------------------------------------------------------------------------
# Usuarios de prueba (contraseñas hasheadas con bcrypt)
# ---------------------------------------------------------------------------
SEED_USERS: list[User] = [
    User(
        id=1,
        username="admin",
        hashed_password=_pwd_context.hash("Admin1234!"),
        role=Role.ADMIN,
        is_active=True,
    ),
    User(
        id=2,
        username="user",
        hashed_password=_pwd_context.hash("User1234!"),
        role=Role.USER,
        is_active=True,
    ),
]


# ---------------------------------------------------------------------------
# Migración de imágenes a Cloudinary
# ---------------------------------------------------------------------------

async def migrate_seed_images(car_repository) -> None:
    """
    Recorre los 20 coches del seed y asegura que cada uno tiene su imagen en Cloudinary.

    Lógica inteligente por arranque:
    - Si el public_id YA EXISTE en Cloudinary: recupera la URL y actualiza el Car (sin subir).
    - Si NO EXISTE: descarga el placeholder y lo sube a Cloudinary.

    Primera ejecución: sube los 20. Arranques posteriores: termina en < 1 segundo.
    """
    from infrastructure.adapters.cloudinary_adapter import CloudinaryAdapter

    adapter = CloudinaryAdapter()
    ok_count = 0
    fail_count = 0

    print("─" * 60)
    print("  Iniciando migración de imágenes a Cloudinary...")
    print("─" * 60)

    skip_count = 0

    async with httpx.AsyncClient(
        timeout=30,
        follow_redirects=True,
        headers={"User-Agent": "PremiumCarCatalog/1.0 (educational project)"},
    ) as client:
        for car in SEED_CARS:
            label = f"[{car.id:02d}] {car.marca} {car.modelo}"

            public_id = (
                f"car_{car.id}_{car.marca.lower().replace(' ', '_')}"
                f"_{car.modelo.lower().replace(' ', '_')}"
            )

            try:
                # ── 1. Comprobar si ya existe en Cloudinary ──────────────────
                existing_url = await asyncio.to_thread(
                    adapter.get_existing_url, public_id
                )
                if existing_url:
                    car_repository.update(car.id, {"imagen_url": existing_url})
                    skip_count += 1
                    print(f"  [IGNORADO] {car.marca} {car.modelo} ya existe en Cloudinary")
                    logger.info("Imagen coche %d ya existe en Cloudinary, omitida", car.id)
                    continue

                # ── 2. No existe: descargar placeholder y subir ──────────────
                response = await client.get(car.imagen_url)
                response.raise_for_status()

                new_url = await asyncio.to_thread(
                    adapter.upload_image,
                    response.content,
                    public_id,
                )

                car_repository.update(car.id, {"imagen_url": new_url})
                ok_count += 1
                print(f"  [SUBIDO] {car.marca} {car.modelo} enviado a Cloudinary")
                logger.info("Migrada imagen coche %d -> %s", car.id, new_url)

            except Exception as exc:  # noqa: BLE001
                fail_count += 1
                print(f"  ❌ ERROR {label}: {exc}")
                logger.warning("No se pudo migrar imagen coche %d: %s", car.id, exc)

    print("─" * 60)
    print(f"  Migración completada: {ok_count} [SUBIDO]  |  {skip_count} [IGNORADO]  |  {fail_count} ❌")
    print("─" * 60)
