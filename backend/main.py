"""
Punto de entrada para ejecutar la API con Uvicorn.
Ejecutar desde el directorio backend/ con: python main.py
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "infrastructure.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
