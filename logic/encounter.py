
import random
from logic.core.pathing import resource_path
from logic.core.cache import get_cache
from logic.core.io import load_json

CACHE_ENCOUNTERS = "encounters"
CACHE_ADVENTURES = "adventures"


def load_encounters():
    file_path = resource_path("Data/encounter.json")

    def loader():
        return load_json(file_path)

    return get_cache(CACHE_ENCOUNTERS, loader)


def load_adventures():
    file_path = resource_path("Data/adv.json")

    def loader():
        return load_json(file_path)

    return get_cache(CACHE_ADVENTURES, loader)


def generate_encounter():
    """Generate random encounter (monster or adventure)."""

    choice_type = random.choices(
        ["monster", "adventure"],
        weights=[0.6, 0.4],
        k=1
    )[0]

    if choice_type == "monster":
        encounters = load_encounters()
        if not encounters:
            raise RuntimeError("Encounter cache failed to load")
        data_enc = random.choice(encounters).copy()
        data_enc["is_monster"] = True
        return data_enc

    adventures = load_adventures()
    if not adventures:
        raise RuntimeError("Adventure cache failed to load")
    data_adv = random.choice(adventures).copy()
    data_adv["is_monster"] = False
    return data_adv
