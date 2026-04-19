import random
from logic.core.generator_base import Generator
from typing import Dict, Any
from logic.core.pathing import resource_path
from logic.core.io import load_json
from logic.core.cache import get_cache
from logic.core.empty_validation_check import validate_list


class CityGenerator(Generator):
    CACHE_KEY = 'city'
    DATA_FILE = "Data/city_template.json"

    def load(self):
        load_json_path = resource_path(self.DATA_FILE)
        return get_cache(self.CACHE_KEY, lambda: load_json(load_json_path))

    def validate_data(self, data: Any) -> None:
        if not isinstance(data, dict) or not data:
            raise RuntimeError("City cache invalid or empty")

    def generate(self, **kwargs) -> Dict[str, Any]:
        data = self.load()
        self.validate_data(data)

        city_name = kwargs.get("city_name")
        if not city_name:
            raise ValueError("city_name is required")

        if city_name not in data:
            raise ValueError(f"Unknown city {city_name}")

        city = data[city_name]

        if not isinstance(city, dict) or not city:
            raise ValueError(f"Invalid city structure: {city_name}")

        # Problems
        validate_list(city["problems"], "City problems")
        problems = random.sample(city["problems"], 2)

        # Goods
        validate_list(city["goods"], "City goods")
        goods = random.sample(city["goods"], 2)

        # Superstitions
        validate_list(city["superstitions"], "City superstitions")
        superstitions = random.choice(city["superstitions"])

        return {
            "city": city_name,
            "problems": problems,
            "superstitions": superstitions,
            "goods": goods
        }

    def get_available_city_names(self):
        data = self.load()
        self.validate_data(data)
        return list(data.keys())


# added to make select City from the list available.
_city_generator = CityGenerator()


def generate_city(city_name):
    return _city_generator.generate(city_name=city_name)


def get_available_city_names():
    return _city_generator.get_available_city_names()
