import random

from logic.core.pathing import resource_path
from logic.core.cache import get_cache
from logic.core.io import load_json

CACHE_KEY = 'loot'


def load_loot():
    file_path = resource_path("Data/loot.json")

    def loader():
        return load_json(file_path)

    return get_cache(CACHE_KEY, loader)


def generate_loot():
    loot = load_loot()

    if not loot:
        raise RuntimeError("Loot cache failed to load")

    if not isinstance(loot, list):
        raise ValueError("Loot must be a list")

    if len(loot) == 0:
        raise ValueError("Loot list is empty")

    item = random.choice(loot)

    if not isinstance(item, dict):
        raise ValueError("Loot item must be dict")

    return item.copy()
