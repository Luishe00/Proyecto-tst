import asyncio
from httpx import AsyncClient
from infrastructure.api.main import app

async def main():
    async with AsyncClient(app=app, base_url='http://test') as client:
        resp = await client.post(
            '/cars',
            headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsInVzZXJfaWQiOjEsImV4cCI6MTc3NTUxMTM1Mn0.onfDX2Ln69Fks4DNF_N7_xz7J-WEdLf7WgTlJ_Cu4DM'},
            data={
                'marca': 'Bugatti',
                'modelo': 'Chiron',
                'cv': '1500',
                'peso': '1995',
                'velocidad_max': '420',
                'precio': '3200000',
                'year': '2024',
                'imagen_url': 'https://example.com/chiron.jpg',
            },
        )
        print(resp.status_code)
        print(resp.text)

asyncio.run(main())
