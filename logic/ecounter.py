import json
import os
import random
import sys


# ---------------- PATH HANDLER ----------------

def resource_path(relative_path):
    """Absolute file path for both dev and exe."""
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS  # PyInstaller
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, relative_path)


# ---------------- CACHE ----------------

_encounter_cache = None
_adventure_cache = None


# ---------------- LOADERS ----------------

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


# ---------------- GENERATOR ----------------

def generate_encounter():
    """Generate random encounter (monster or adventure)."""

    choice_type = random.choices(
        ["monster", "adventure"],
        weights=[0.6, 0.4],
        k=1
    )[0]

    if choice_type == "monster":
        enc = random.choice(get_encounters())
        enc = enc.copy()  # important: avoid mutating cached data
        enc["is_monster"] = True
        return enc

    adv = random.choice(get_adventures())
    adv = adv.copy()
    adv["is_monster"] = False
    return adv
