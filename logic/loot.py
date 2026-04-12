import os
import sys
import random
import json


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS  # exe
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, relative_path)


loot_file = resource_path(os.path.join('Data', 'loot.json'))

_loot_cache = None


def get_loot_data():
    global _loot_cache

    if _loot_cache is None:
        file_path = resource_path("Data/loot.json")
        with open(file_path, encoding="utf-8") as f:
            _loot_cache = json.load(f)
    return _loot_cache


def generate_loot():
    loot = get_loot_data()
    assert loot is not None, "Loot cache not loaded"
    return random.choice(loot)
