import json
import os
import random

encounter_file = os.path.join(
    os.path.dirname(__file__), 'Data', 'encounter.json')
adventure_file = os.path.join(os.path.dirname(__file__), 'Data', 'adv.json')

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
        # jeśli potwór ma CR, traktujemy go jako monster
        if enc.get('cr') is not None:
            enc['is_monster'] = True
            return enc
        else:
            # fallback na adventure jeśli CR null
            adv = random.choice(adventures)
            adv['is_monster'] = False
            return adv
    else:
        adv = random.choice(adventures)
        adv['is_monster'] = False
        return adv
