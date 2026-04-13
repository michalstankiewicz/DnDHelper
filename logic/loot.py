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
    assert loot is not None, "Loot cache not loaded"
    return random.choice(loot)
