import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# 1. Configuración inicial
load_dotenv()
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
     api_key=os.getenv("CLOUDINARY_API_KEY"),
     api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Ruta exacta de tu imagen
PATH_TO_IMAGES = r'C:\Users\luish\OneDrive\Escritorio\Fotos Proyecto'

def normalize_name(name):
    """Convierte 'Ferrari_LaFerrari' o 'Porsche 911' en 'ferrari-laferrari'"""
    # Quitar extensión, pasar a minúsculas, cambiar espacios y guiones bajos por guiones
    clean_name = name.lower().replace(" ", "-").replace("_", "-")
    # Evitar dobles guiones si ya había un guion y un espacio juntos
    while "--" in clean_name:
        clean_name = clean_name.replace("--", "-")
    return clean_name

def process_catalog():
    print("🚀 Iniciando normalización y subida...")
    final_mapping = {}

    # Listar archivos
    files = [f for f in os.listdir(PATH_TO_IMAGES) if f.endswith((".jpg", ".png", ".jpeg"))]

    for filename in files:
        old_path = os.path.join(PATH_TO_IMAGES, filename)
        
        # Obtener nombre y extensión
        name_part, extension = os.path.splitext(filename)
        
        # 2. Normalizar nombre
        new_name = normalize_name(name_part)
        new_filename = f"{new_name}{extension}"
        new_path = os.path.join(PATH_TO_IMAGES, new_filename)

        # 3. Renombrar archivo localmente (opcional, pero recomendado para orden)
        if old_path != new_path:
            os.rename(old_path, new_path)
            print(f"📦 Renombrado: {filename} -> {new_filename}")

        # 4. Subir a Cloudinary
        try:
            print(f"☁️ Subiendo {new_name}...")
            response = cloudinary.uploader.upload(
                new_path,
                folder="premium_cars_catalog",
                public_id=new_name,
                overwrite=True # Si ya existe, lo actualiza
            )
            
            # Guardar la URL para el código final
            final_mapping[new_name] = response.get('secure_url')
            print(f"✅ Éxito: {new_name}")
            
        except Exception as e:
            print(f"❌ Error con {new_name}: {e}")

    # 5. Resultado final para copiar y pegar
    print("\n" + "="*50)
    print("COPIA ESTO EN TU IN-MEMORY REPOSITORY")
    print("="*50)
    for car, url in final_mapping.items():
        print(f"'{car}': '{url}',")

if __name__ == "__main__":
    process_catalog()