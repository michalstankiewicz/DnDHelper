
import json
import os
import random
from dice import roll_dice

encounter_file = os.path.join(
    os.path.dirname(__file__), 'Data', 'encounter.json')


with open(encounter_file, 'r', encoding='utf-8') as f:
    encounters = json.load(f)  # globalna lista


def generate_encounter():
    encounter = random.choice(encounters)
    return encounter  # zwracamy pojedynczy encounter
