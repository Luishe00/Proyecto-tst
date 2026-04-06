"""
Adaptador de persistencia en memoria para el repositorio de coches.
Implementa CarRepository usando un diccionario de Python como almacén.
"""
from typing import Dict, List, Optional

from domain.entities.car import Car
from domain.ports.car_repository import CarRepository


class InMemoryCarRepository(CarRepository):
    """Repositorio de coches en memoria. 100% portable, sin dependencias externas."""

    def __init__(self, load_seed: bool = False) -> None:
        self._storage: Dict[int, Car] = {}
        self._next_id: int = 1
        if load_seed:
            self._seed()

    def _seed(self) -> None:
        urls = {
            "astonmartin-db11amr": "https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501561/premium_cars_catalog/astonmartin-db11amr.jpg",
            "astonmartin-dbs-superleggera": "https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501562/premium_cars_catalog/astonmartin-dbs-superleggera.jpg",
            "astonmartin-valkyrie": "https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501562/premium_cars_catalog/astonmartin-valkyrie.jpg",
            "astonmartin-vantage-v12": "https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501563/premium_cars_catalog/astonmartin-vantage-v12.jpg",
            "ferrari-f8-tributo": "https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501564/premium_cars_catalog/ferrari-f8-tributo.jpg",
            "ferrari-laferrari": "https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501564/premium_cars_catalog/ferrari-laferrari.jpg",
            "ferrari-roma": "https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501565/premium_cars_catalog/ferrari-roma.jpg",
            "ferrari-sf90-stradale": "https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501566/premium_cars_catalog/ferrari-sf90-stradale.jpg",
            "lamborghin-huracán-evo": "https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501566/premium_cars_catalog/lamborghin-hurac%C3%A1n-evo.jpg",
            "lamborghini-aventador-svj": "https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501567/premium_cars_catalog/lamborghini-aventador-svj.jpg",
            "lamborghini-sián-fkp-37": "https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501569/premium_cars_catalog/lamborghini-si%C3%A1n-fkp-37.jpg",
            "lamborghini-urus-performante": "https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501569/premium_cars_catalog/lamborghini-urus-performante.jpg",
            "mclaren-720s": "https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501570/premium_cars_catalog/mclaren-720s.jpg",
            "mclaren-senna": "https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501571/premium_cars_catalog/mclaren-senna.jpg",
            "mclaren-speedtail": "https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501572/premium_cars_catalog/mclaren-speedtail.png",
            "porsche-918-spyder-2018": "https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501573/premium_cars_catalog/porsche-918-spyder-2018.jpg",
            "porsche-cayenne-turbo-gt": "https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501573/premium_cars_catalog/porsche-cayenne-turbo-gt.jpg",
            "porsche-panamera-turbo-s": "https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501574/premium_cars_catalog/porsche-panamera-turbo-s.jpg",
            "porsche-taycan-turbo-s": "https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501575/premium_cars_catalog/porsche-taycan-turbo-s.jpg",
            "porsche911-gt3-rs": "https://res.cloudinary.com/dsmvz3ruy/image/upload/v1775501576/premium_cars_catalog/porsche911-gt3-rs.jpg",
        }

        initial_cars = [
            {
                "key": "astonmartin-db11amr",
                "marca": "Aston Martin",
                "modelo": "DB11 AMR",
                "precio": 241500.0,
                "cv": 639,
                "peso": 1870,
                "velocidad_max": 334,
                "year": 2022,
            },
            {
                "key": "astonmartin-dbs-superleggera",
                "marca": "Aston Martin",
                "modelo": "DBS Superleggera",
                "precio": 316000.0,
                "cv": 725,
                "peso": 1845,
                "velocidad_max": 340,
                "year": 2021,
            },
            {
                "key": "astonmartin-valkyrie",
                "marca": "Aston Martin",
                "modelo": "Valkyrie",
                "precio": 3000000.0,
                "cv": 1160,
                "peso": 1030,
                "velocidad_max": 402,
                "year": 2023,
            },
            {
                "key": "astonmartin-vantage-v12",
                "marca": "Aston Martin",
                "modelo": "Vantage V12",
                "precio": 215000.0,
                "cv": 700,
                "peso": 1795,
                "velocidad_max": 322,
                "year": 2023,
            },
            {
                "key": "ferrari-f8-tributo",
                "marca": "Ferrari",
                "modelo": "F8 Tributo",
                "precio": 276000.0,
                "cv": 720,
                "peso": 1435,
                "velocidad_max": 340,
                "year": 2022,
            },
            {
                "key": "ferrari-laferrari",
                "marca": "Ferrari",
                "modelo": "LaFerrari",
                "precio": 1800000.0,
                "cv": 963,
                "peso": 1585,
                "velocidad_max": 352,
                "year": 2016,
            },
            {
                "key": "ferrari-roma",
                "marca": "Ferrari",
                "modelo": "Roma",
                "precio": 247171.0,
                "cv": 620,
                "peso": 1570,
                "velocidad_max": 320,
                "year": 2023,
            },
            {
                "key": "ferrari-sf90-stradale",
                "marca": "Ferrari",
                "modelo": "SF90 Stradale",
                "precio": 465000.0,
                "cv": 1000,
                "peso": 1570,
                "velocidad_max": 340,
                "year": 2023,
            },
            {
                "key": "lamborghin-huracán-evo",
                "marca": "Lamborghini",
                "modelo": "Huracán EVO",
                "precio": 259000.0,
                "cv": 640,
                "peso": 1422,
                "velocidad_max": 325,
                "year": 2022,
            },
            {
                "key": "lamborghini-aventador-svj",
                "marca": "Lamborghini",
                "modelo": "Aventador SVJ",
                "precio": 445000.0,
                "cv": 770,
                "peso": 1525,
                "velocidad_max": 350,
                "year": 2021,
            },
            {
                "key": "lamborghini-sián-fkp-37",
                "marca": "Lamborghini",
                "modelo": "Sián FKP 37",
                "precio": 3600000.0,
                "cv": 819,
                "peso": 1595,
                "velocidad_max": 350,
                "year": 2021,
            },
            {
                "key": "lamborghini-urus-performante",
                "marca": "Lamborghini",
                "modelo": "Urus Performante",
                "precio": 280000.0,
                "cv": 666,
                "peso": 2150,
                "velocidad_max": 306,
                "year": 2023,
            },
            {
                "key": "mclaren-720s",
                "marca": "McLaren",
                "modelo": "720S",
                "precio": 310000.0,
                "cv": 720,
                "peso": 1419,
                "velocidad_max": 341,
                "year": 2021,
            },
            {
                "key": "mclaren-senna",
                "marca": "McLaren",
                "modelo": "Senna",
                "precio": 965000.0,
                "cv": 800,
                "peso": 1198,
                "velocidad_max": 335,
                "year": 2020,
            },
            {
                "key": "mclaren-speedtail",
                "marca": "McLaren",
                "modelo": "Speedtail",
                "precio": 2200000.0,
                "cv": 1070,
                "peso": 1430,
                "velocidad_max": 403,
                "year": 2020,
            },
            {
                "key": "porsche-918-spyder-2018",
                "marca": "Porsche",
                "modelo": "918 Spyder",
                "precio": 875000.0,
                "cv": 887,
                "peso": 1674,
                "velocidad_max": 345,
                "year": 2018,
            },
            {
                "key": "porsche-cayenne-turbo-gt",
                "marca": "Porsche",
                "modelo": "Cayenne Turbo GT",
                "precio": 212000.0,
                "cv": 659,
                "peso": 2220,
                "velocidad_max": 305,
                "year": 2023,
            },
            {
                "key": "porsche-panamera-turbo-s",
                "marca": "Porsche",
                "modelo": "Panamera Turbo S",
                "precio": 217000.0,
                "cv": 630,
                "peso": 2070,
                "velocidad_max": 315,
                "year": 2022,
            },
            {
                "key": "porsche-taycan-turbo-s",
                "marca": "Porsche",
                "modelo": "Taycan Turbo S",
                "precio": 196000.0,
                "cv": 761,
                "peso": 2295,
                "velocidad_max": 260,
                "year": 2023,
            },
            {
                "key": "porsche911-gt3-rs",
                "marca": "Porsche",
                "modelo": "911 GT3 RS",
                "precio": 265000.0,
                "cv": 525,
                "peso": 1450,
                "velocidad_max": 296,
                "year": 2024,
            },
        ]

        for car_data in initial_cars:
            self.create(
                Car(
                    marca=car_data["marca"],
                    modelo=car_data["modelo"],
                    precio=float(car_data["precio"]),
                    cv=int(car_data["cv"]),
                    peso=int(car_data["peso"]),
                    velocidad_max=int(car_data["velocidad_max"]),
                    imagen_url=urls[car_data["key"]],
                    year=int(car_data["year"]),
                )
            )

    def get_all(self) -> List[Car]:
        """Devuelve todos los coches almacenados."""
        return list(self._storage.values())

    def get_by_id(self, car_id: int) -> Optional[Car]:
        """Devuelve el coche con el ID indicado o None si no existe."""
        return self._storage.get(car_id)

    def create(self, car: Car) -> Car:
        """
        Persiste un coche nuevo.
        Si car.id > 0 (seed data), usa ese ID.
        Si car.id == 0, asigna el siguiente ID disponible.
        """
        if car.id > 0:
            stored_car = car
            self._storage[car.id] = stored_car
            if car.id >= self._next_id:
                self._next_id = car.id + 1
        else:
            stored_car = car.model_copy(update={"id": self._next_id})
            self._storage[self._next_id] = stored_car
            self._next_id += 1
        return stored_car

    def update(self, car_id: int, data: Dict) -> Optional[Car]:
        """Actualiza los campos indicados de un coche. Devuelve el coche actualizado o None."""
        if car_id not in self._storage:
            return None
        updated_car = self._storage[car_id].model_copy(update=data)
        self._storage[car_id] = updated_car
        return updated_car

    def delete(self, car_id: int) -> bool:
        """Elimina un coche por ID. Devuelve True si existía y fue eliminado."""
        if car_id not in self._storage:
            return False
        del self._storage[car_id]
        return True
