import random
from logic.core.pathing import resource_path
from logic.core.cache import get_cache
from logic.core.io import load_json
from logic.core.empty_validation_check import validate_item, validate_list

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

    validate_list(loot, "Loot")

    item = random.choice(loot)

    validate_item(item, "Loot item must be dict")
