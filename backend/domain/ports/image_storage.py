"""
Puerto (interfaz) para el almacenamiento de imágenes.
Define el contrato que deben cumplir los adaptadores de storage.
"""
from abc import ABC, abstractmethod


class ImageStorage(ABC):
    """Interfaz abstracta para servicios de almacenamiento de imágenes."""

    @abstractmethod
    def upload_image(self, file_content: bytes, filename: str) -> str:
        """
        Sube una imagen al servicio de almacenamiento.

        Args:
            file_content: Contenido binario de la imagen.
            filename: Nombre del archivo (se usa como public_id).

        Returns:
            URL pública de la imagen subida.
        """
