import json
import os
import random
import sys


def resource_path(relative_path):
    """Absolute file path for both dev and exe."""
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, relative_path)


_encounter_cache = None
_adventure_cache = None


def get_encounters():
    global _encounter_cache

    if _encounter_cache is None:
        file_path = resource_path("Data/encounter.json")
        with open(file_path, encoding="utf-8") as f:
            _encounter_cache = json.load(f)

    return _encounter_cache


def get_adventures():
    global _adventure_cache

    if _adventure_cache is None:
        file_path = resource_path("Data/adv.json")
        with open(file_path, encoding="utf-8") as f:
            _adventure_cache = json.load(f)

    return _adventure_cache


def generate_encounter():
    """Generate random encounter (monster or adventure)."""

    choice_type = random.choices(
        ["monster", "adventure"],
        weights=[0.6, 0.4],
        k=1
    )[0]

    if choice_type == "monster":
        enc = random.choice(get_encounters())
        assert _encounter_cache is not None, "Encounter Cache not loaded"
        enc = enc.copy()
        enc["is_monster"] = True
        return enc

    adv = random.choice(get_adventures())
    assert _adventure_cache is not None, "Adventure Cache not loaded"
    adv = adv.copy()
    adv["is_monster"] = False
    return adv
