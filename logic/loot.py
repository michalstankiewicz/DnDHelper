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

with open(loot_file, 'r', encoding='utf-8') as f:
    loot_data = json.load(f)  # global list of loot items


def generate_loot():
    loot_item = random.choice(loot_data)
    return loot_item  # one item is returned
