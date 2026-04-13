from logic.core.pathing import resource_path
from logic.core.cache import get_cache
import json
import random

CACHE_KEY = "npc"


def _load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_npc():
    file_path = resource_path("Data/npc.json")

    def loader():
        return _load_json(file_path)

    return get_cache(CACHE_KEY, loader)


def generate_npc():
    npc_data = load_npc()
    assert npc_data is not None, "NPC cache not loaded"
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
