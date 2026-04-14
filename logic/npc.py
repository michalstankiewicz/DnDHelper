from logic.core.pathing import resource_path
from logic.core.cache import get_cache
from logic.core.io import load_json
import random

CACHE_KEY = "npc"


def load_npc():
    file_path = resource_path("Data/npc.json")

    def loader():
        return load_json(file_path)

    return get_cache(CACHE_KEY, loader)


def generate_npc():
    npc_data = load_npc()
    if not npc_data:
        raise RuntimeError("Npc cache failed to load")
    race = random.choice(list(npc_data["races"]))
    gender = random.choice(["male", "female"])

    names = npc_data["races"].get(race, {}).get(gender, [])
    if not names:
        raise ValueError(f"Missing names for {race}/{gender}")

    name = random.choice(names)
    surname = random.choice(npc_data["surnames"])
    trait = random.choice(npc_data["traits"])
    hook = random.choice(npc_data["hooks"])

    return {
        "race": race,
        "gender": gender,
        "name": name,
        "surname": surname,
        "trait": trait,
        "hook": hook
    }
