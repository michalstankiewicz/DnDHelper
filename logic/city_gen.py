import json
import random
from logic.core.pathing import resource_path
from logic.core.io import load_json
from logic.core.cache import get_cache

CACHE_KEY = 'city'


def load_city():
    file_path = resource_path("Data/city_template.json")

    def loader():
        return load_json(file_path)

    return get_cache(CACHE_KEY, loader)


def city_gen(city_name):
    """City generator"""
    data = load_city()
    if not isinstance(data, dict) or not data:
        raise RuntimeError("City cache invalid or empty")
    city = data[city_name]
    problems = random.sample(city["problems"], 2)
    goods = random.sample(city["goods"], 2)
    superstitions = random.sample(city["superstitions"], 1)[0]

    return {
        "city": city_name,
        "problems": problems,
        "superstitions": superstitions,
        "goods": goods
    }
