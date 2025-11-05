import random
from datetime import datetime

from ..utils import logger, FileManager
from .world_cities_data import world_cities_data, world_cities


class Fetcher:

    def __init__(self):
        self.file_manager = FileManager()

    @staticmethod
    def _add_population_noise(population) -> int:
        noise = random.random()
        if random.choice([True, False]):
            noise = noise + 1
        return int(population * noise)


    def _format_data(self, city_data: dict):
        city_data["stats"]["country"] = city_data["stats"]["country"].lower().strip()
        city_data["stats"]["population"] = self._add_population_noise(
            population=city_data["stats"]["population"]
        )
        return {
            "name": city_data["name"].lower().strip(),
            "stats": city_data["stats"]
        }


    def fetch_fake_data(self) -> dict:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        random_city = random.choice(world_cities)
        city_stats = world_cities_data[random_city]
        city_data = {
            "name": random_city,
            "stats": city_stats,
        }
        data = {
            "data": self._format_data(city_data=city_data),
            "timestamp": now_str,
        }

        return data