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
    # City name
    if city_name not in data:
        raise ValueError(f"Unknown city {city_name}")
    city = data[city_name]
    if not isinstance(city, dict) or not city:
        raise ValueError(f"Invalid city structure: {city_name}")

    # Problems
    if not isinstance(city["problems"], list):
        raise ValueError(f"City 'problems' must be a list")
    if len(city["problems"]) < 2:
        raise ValueError("City 'problems' must contain at least 2 items")
    problems = random.sample(city["problems"], 2)

    # Goods
    if not isinstance(city["goods"], list):
        raise ValueError(f"City 'goods' must be a list")
    if len(city["goods"]) < 2:
        raise ValueError("City 'goods' must contain at least 2 items")
    goods = random.sample(city["goods"], 2)

    # Superstitions
    if not isinstance(city["superstitions"], list):
        raise ValueError("City 'superstitions' must be a list")
    if len(city["superstitions"]) < 1:
        raise ValueError("City 'superstitions' must contain at least 1 item")
    superstitions = random.sample(city["superstitions"], 1)[0]

    return {
        "city": city_name,
        "problems": problems,
        "superstitions": superstitions,
        "goods": goods
    }
