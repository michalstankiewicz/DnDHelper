import random
from logic.core.pathing import resource_path
from logic.core.io import load_json
from logic.core.cache import get_cache
from logic.core.empty_validation_check import validate_item, validate_list

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
    validate_list(city["problems"], "City problems")
    problems = random.sample(city["problems"], 2)

    # Goods
    validate_list(city["goods"], "City goods")
    goods = random.sample(city["goods"], 2)

    # Superstitions
    validate_list(city["superstitions"], "City superstitions")
    superstitions = random.sample(city["superstitions"], 1)[0]

    return {
        "city": city_name,
        "problems": problems,
        "superstitions": superstitions,
        "goods": goods
    }
