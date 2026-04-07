import json
import os
import random
import sys


def resource_path(relative_path):
    """Absolute file path for both dev and exe."""
    try:
        base_path = sys._MEIPASS  # for exe
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))  # if dev

    return os.path.join(base_path, relative_path)


encounter_file = resource_path(os.path.join('Data', 'encounter.json'))
adventure_file = resource_path(os.path.join('Data', 'adv.json'))

with open(encounter_file, 'r', encoding='utf-8') as f:
    encounters = json.load(f)

with open(adventure_file, 'r', encoding='utf-8') as f:
    adventures = json.load(f)


def generate_encounter():
    """Generate random encounter, either a monster or an adventure."""
    # weighted random choice: 60% monster, 40% adventure
    choice_type = random.choices(
        ['monster', 'adventure'],
        weights=[0.6, 0.4],
        k=1
    )[0]

    if choice_type == 'monster':
        enc = random.choice(encounters)
        #  CR = monster encounter
        if enc.get('cr') is not None:
            enc['is_monster'] = True
            return enc
        else:
            # if  CR is null = adventure
            adv = random.choice(adventures)
            adv['is_monster'] = False
            return adv
    else:
        adv = random.choice(adventures)
        adv['is_monster'] = False
        return adv
