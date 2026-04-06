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
# 20 Coches Premium (4 por marca)
# ---------------------------------------------------------------------------
SEED_CARS: list[Car] = [
    # ── Porsche ─────────────────────────────────────────────────────────────
    Car(
        id=1,
        marca="Porsche",
        modelo="911 GT3 RS",
        cv=525,
        peso=1450,
        velocidad_max=296,
        precio=239700,
        imagen_url="https://placehold.jp/24/003366/ffffff/1280x720.png?text=Porsche_911_GT3_RS",
        year=2022,
    ),
    Car(
        id=2,
        marca="Porsche",
        modelo="Taycan Turbo S",
        cv=761,
        peso=2370,
        velocidad_max=260,
        precio=185456,
        imagen_url="https://placehold.jp/24/003366/ffffff/1280x720.png?text=Porsche_Taycan_Turbo_S",
        year=2021,
    ),
    Car(
        id=3,
        marca="Porsche",
        modelo="918 Spyder",
        cv=887,
        peso=1674,
        velocidad_max=345,
        precio=845000,
        imagen_url="https://placehold.jp/24/003366/ffffff/1280x720.png?text=Porsche_918_Spyder",
        year=2018,
    ),
    Car(
        id=4,
        marca="Porsche",
        modelo="Cayenne Turbo GT",
        cv=640,
        peso=2195,
        velocidad_max=300,
        precio=186000,
        imagen_url="https://placehold.jp/24/003366/ffffff/1280x720.png?text=Porsche_Cayenne_Turbo_GT",
        year=2022,
    ),
    Car(
        id=5,
        marca="Porsche",
        modelo="Panamera Turbo S",
        cv=630,
        peso=2220,
        velocidad_max=315,
        precio=188600,
        imagen_url="https://placehold.jp/24/003366/ffffff/1280x720.png?text=Porsche_Panamera_Turbo_S",
        year=2021,
    ),
    # ── Ferrari ──────────────────────────────────────────────────────────────
    Car(
        id=6,
        marca="Ferrari",
        modelo="SF90 Stradale",
        cv=1000,
        peso=1570,
        velocidad_max=340,
        precio=507000,
        imagen_url="https://placehold.jp/24/cc0000/ffffff/1280x720.png?text=Ferrari_SF90_Stradale",
        year=2020,
    ),
    Car(
        id=7,
        marca="Ferrari",
        modelo="488 Pista",
        cv=720,
        peso=1385,
        velocidad_max=340,
        precio=280000,
        imagen_url="https://placehold.jp/24/cc0000/ffffff/1280x720.png?text=Ferrari_488_Pista",
        year=2018,
    ),
    Car(
        id=8,
        marca="Ferrari",
        modelo="LaFerrari",
        cv=963,
        peso=1255,
        velocidad_max=350,
        precio=1300000,
        imagen_url="https://placehold.jp/24/cc0000/ffffff/1280x720.png?text=Ferrari_LaFerrari",
        year=2018,
    ),
    Car(
        id=9,
        marca="Ferrari",
        modelo="F8 Tributo",
        cv=720,
        peso=1330,
        velocidad_max=340,
        precio=276000,
        imagen_url="https://placehold.jp/24/cc0000/ffffff/1280x720.png?text=Ferrari_F8_Tributo",
        year=2020,
    ),
    Car(
        id=10,
        marca="Ferrari",
        modelo="Roma",
        cv=620,
        peso=1472,
        velocidad_max=320,
        precio=222000,
        imagen_url="https://placehold.jp/24/cc0000/ffffff/1280x720.png?text=Ferrari_Roma",
        year=2021,
    ),
    # ── Lamborghini ───────────────────────────────────────────────────────────
    Car(
        id=11,
        marca="Lamborghini",
        modelo="Aventador SVJ",
        cv=770,
        peso=1525,
        velocidad_max=350,
        precio=420000,
        imagen_url="https://placehold.jp/24/ff6600/ffffff/1280x720.png?text=Lamborghini_Aventador_SVJ",
        year=2019,
    ),
    Car(
        id=12,
        marca="Lamborghini",
        modelo="Huracán EVO",
        cv=640,
        peso=1422,
        velocidad_max=325,
        precio=212000,
        imagen_url="https://placehold.jp/24/ff6600/ffffff/1280x720.png?text=Lamborghini_Huracan_EVO",
        year=2020,
    ),
    Car(
        id=13,
        marca="Lamborghini",
        modelo="Urus Performante",
        cv=666,
        peso=2150,
        velocidad_max=306,
        precio=275000,
        imagen_url="https://placehold.jp/24/ff6600/ffffff/1280x720.png?text=Lamborghini_Urus_Performante",
        year=2022,
    ),
    Car(
        id=14,
        marca="Lamborghini",
        modelo="Sián FKP 37",
        cv=819,
        peso=1595,
        velocidad_max=350,
        precio=3300000,
        imagen_url="https://placehold.jp/24/ff6600/ffffff/1280x720.png?text=Lamborghini_Sian_FKP_37",
        year=2020,
    ),
    Car(
        id=15,
        marca="Lamborghini",
        modelo="Revuelto",
        cv=1015,
        peso=1772,
        velocidad_max=350,
        precio=517000,
        imagen_url="https://placehold.jp/24/ff6600/ffffff/1280x720.png?text=Lamborghini_Revuelto",
        year=2023,
    ),
    # ── Aston Martin ─────────────────────────────────────────────────────────
    Car(
        id=16,
        marca="Aston Martin",
        modelo="DBS Superleggera",
        cv=725,
        peso=1693,
        velocidad_max=340,
        precio=265000,
        imagen_url="https://placehold.jp/24/004d40/ffffff/1280x720.png?text=AstonMartin_DBS_Superleggera",
        year=2018,
    ),
    Car(
        id=17,
        marca="Aston Martin",
        modelo="Vantage V12",
        cv=700,
        peso=1530,
        velocidad_max=330,
        precio=190000,
        imagen_url="https://placehold.jp/24/004d40/ffffff/1280x720.png?text=AstonMartin_Vantage_V12",
        year=2022,
    ),
    Car(
        id=18,
        marca="Aston Martin",
        modelo="Valkyrie",
        cv=1160,
        peso=1000,
        velocidad_max=402,
        precio=3200000,
        imagen_url="https://placehold.jp/24/004d40/ffffff/1280x720.png?text=AstonMartin_Valkyrie",
        year=2021,
    ),
    Car(
        id=19,
        marca="Aston Martin",
        modelo="DB11 AMR",
        cv=630,
        peso=1760,
        velocidad_max=335,
        precio=220000,
        imagen_url="https://placehold.jp/24/004d40/ffffff/1280x720.png?text=AstonMartin_DB11_AMR",
        year=2019,
    ),
    Car(
        id=20,
        marca="Aston Martin",
        modelo="Vulcan",
        cv=820,
        peso=1350,
        velocidad_max=362,
        precio=2300000,
        imagen_url="https://placehold.jp/24/004d40/ffffff/1280x720.png?text=AstonMartin_Vulcan",
        year=2018,
    ),
    # ── McLaren ───────────────────────────────────────────────────────────────
    Car(
        id=21,
        marca="McLaren",
        modelo="P1",
        cv=916,
        peso=1395,
        velocidad_max=350,
        precio=1150000,
        imagen_url="https://placehold.jp/24/e65100/ffffff/1280x720.png?text=McLaren_P1",
        year=2018,
    ),
    Car(
        id=22,
        marca="McLaren",
        modelo="Senna",
        cv=800,
        peso=1198,
        velocidad_max=340,
        precio=750000,
        imagen_url="https://placehold.jp/24/e65100/ffffff/1280x720.png?text=McLaren_Senna",
        year=2019,
    ),
    Car(
        id=23,
        marca="McLaren",
        modelo="720S",
        cv=720,
        peso=1283,
        velocidad_max=341,
        precio=235000,
        imagen_url="https://placehold.jp/24/e65100/ffffff/1280x720.png?text=McLaren_720S",
        year=2021,
    ),
    Car(
        id=24,
        marca="McLaren",
        modelo="Artura",
        cv=680,
        peso=1395,
        velocidad_max=330,
        precio=225000,
        imagen_url="https://placehold.jp/24/e65100/ffffff/1280x720.png?text=McLaren_Artura",
        year=2022,
    ),
    Car(
        id=25,
        marca="McLaren",
        modelo="Speedtail",
        cv=1050,
        peso=1430,
        velocidad_max=403,
        precio=2100000,
        imagen_url="https://placehold.jp/24/e65100/ffffff/1280x720.png?text=McLaren_Speedtail",
        year=2020,
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
