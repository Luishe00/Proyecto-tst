"""
Adaptador de infraestructura para Cloudinary.
Implementa el puerto ImageStorage usando la librería oficial de Cloudinary.
"""
import io
import os
from typing import Optional

import cloudinary
import cloudinary.api
import cloudinary.exceptions
import cloudinary.uploader
from dotenv import load_dotenv

from domain.ports.image_storage import ImageStorage

load_dotenv()


class CloudinaryAdapter(ImageStorage):
    """Adaptador que sube imágenes a Cloudinary con transformaciones optimizadas."""

    def __init__(self) -> None:
        cloudinary.config(
            cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
            api_key=os.getenv("CLOUDINARY_API_KEY"),
            api_secret=os.getenv("CLOUDINARY_API_SECRET"),
            secure=True,
        )

    def upload_image(self, file_content: bytes, filename: str) -> str:
        """
        Sube una imagen a Cloudinary aplicando transformaciones y devuelve la URL pública.

        Transformaciones aplicadas: w_1280, h_720, c_fill, g_auto, f_auto, q_auto.
        Carpeta de destino: premium-cars.
        """
        result = cloudinary.uploader.upload(
            io.BytesIO(file_content),
            folder="premium-cars",
            public_id=filename,
            overwrite=True,
            transformation=[
                {
                    "width": 1280,
                    "height": 720,
                    "crop": "fill",
                    "gravity": "auto",
                    "fetch_format": "auto",
                    "quality": "auto",
                }
            ],
        )
        return result["secure_url"]

    def get_existing_url(self, public_id: str) -> Optional[str]:
        """
        Comprueba si un recurso ya existe en Cloudinary por su public_id.

        Returns:
            La URL segura del recurso si existe, None en caso contrario.
        """
        try:
            resource = cloudinary.api.resource(f"premium-cars/{public_id}")
            return resource["secure_url"]
        except cloudinary.exceptions.NotFound:
            return None
