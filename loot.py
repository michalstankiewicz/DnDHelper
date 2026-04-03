import os
import random
import json

loot_file = os.path.join(os.path.dirname(__file__), 'Data', 'loot.json')


with open(loot_file, 'r', encoding='utf-8') as f:
    loot_data = json.load(f)  # globalna lista


def generate_loot():
    loot_item = random.choice(loot_data)
    return loot_item  # zwracamy pojedynczy item
