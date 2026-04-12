import json
import os
import sys
import random


def resource_path(relative_path):
    """Absolute file path for both dev and exe."""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS  # exe
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, relative_path)


_npc_cache = None


def get_npc_data():
    global _npc_cache
    if _npc_cache is None:
        npc_file = resource_path(os.path.join('Data', 'npc.json'))
        with open(npc_file, 'r', encoding='utf-8') as f:
            _npc_cache = json.load(f)  # global list of NPCs
    return _npc_cache


def generate_npc():
    npc_data = get_npc_data()
    assert npc_data is not None, "Cache not loaded!"
    race = random.choice(list(npc_data["races"]))
    gender = random.choice(["male", "female"])
    name = random.choice(npc_data["races"][race][gender])
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
