from logic.core.pathing import resource_path
import json


def load_spell_json():
    file_path = resource_path("Data/spells.json")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def search_spells(name_filter="", level_filter="", class_filter=""):
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

        desc = s.get('description', '').replace('\n', ' ')

        results.append(
            f"{s['name']} | Level: {s.get('level')} | "
            f"Description: {desc} | Classes: {', '.join(s.get('classes', []))}"
        )

    return results
