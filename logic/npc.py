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


npc_file = resource_path(os.path.join('Data', 'npc.json'))

with open(npc_file, 'r', encoding='utf-8') as f:
    npc_data = json.load(f)  # global list of NPCs


def generate_npc():
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
