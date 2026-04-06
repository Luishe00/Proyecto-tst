"""
Manejador de tokens JWT.
Responsable de crear y verificar tokens de acceso para la autenticación OAuth2.
"""
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from jose import JWTError, jwt

# En producción, cargar desde variables de entorno (ej: os.environ["SECRET_KEY"])
SECRET_KEY: str = "premium-cars-secret-key-2024-change-in-production"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


class JWTHandler:
    """Gestiona la creación y decodificación de tokens JWT."""

    def create_access_token(
        self,
        data: Dict,
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        """
        Crea un token JWT firmado con los datos proporcionados.

        Args:
            data: Payload a incluir en el token (ej: sub, role, user_id).
            expires_delta: Tiempo de expiración personalizado. Si es None, usa el valor por defecto.

        Returns:
            Token JWT codificado como string.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (
            expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    def decode_token(self, token: str) -> Dict:
        """
        Decodifica y verifica un token JWT.

        Args:
            token: Token JWT en formato string.

        Returns:
            Diccionario con el payload del token.

        Raises:
            JWTError: Si el token es inválido o ha expirado.
        """
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
