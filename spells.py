import json
import os
import sys


def load_spell_json():
    """Load spells.json from Data folder, works both in dev and exe."""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
    json_file = os.path.join(base_path, 'Data', 'spells.json')
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def search_spells(name_filter="", level_filter="", class_filter=""):
    """
    Return a list of filtered spells.
    name_filter, level_filter, class_filter are strings.
    """
    results = []
    spells = load_spell_json()

    name_filter = name_filter.lower() if name_filter else ""
    class_filter = class_filter.lower() if class_filter else ""

    for s in spells:
        if name_filter and name_filter not in s['name'].lower():
            continue
        if level_filter and str(s.get('level', '')) != level_filter:
            continue
        if class_filter and class_filter not in [c.lower() for c in s.get('classes', [])]:
            continue
        if s.get('description'):
            s['description'] = s['description'].replace('\n', ' ')
            continue
        results.append(
            f"{s['name']} | Level: {s.get('level')} | Description: {s.get('description')}  | Classes: {', '.join(s.get('classes', []))}"
        )

    return results
