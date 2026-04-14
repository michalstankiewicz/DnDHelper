from logic.core.pathing import resource_path
from logic.core.cache import get_cache
from logic.core.io import load_json
from logic.core.empty_validation_check import validate_item, validate_list


CACHE_SPELLS = "spells"


def load_spell_json():
    file_path = resource_path("Data/spells.json")

    def loader():
        return load_json(file_path)
    return get_cache(CACHE_SPELLS, loader)


def search_spells(name_filter="", level_filter="", class_filter=""):

    spells = load_spell_json()
    if not spells:
        raise RuntimeError("Spells cache failed to load")

    validate_list(spells, "Spells")

    results = []
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
