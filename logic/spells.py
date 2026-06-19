import random
from logic.core.pathing import resource_path
from logic.core.cache import get_cache
from logic.core.io import load_json
from logic.core.empty_validation_check import validate_item, validate_list
from logic.core.generator_base import Generator
from typing import Dict, Any, List


CACHE_SPELLS = "spells"


def load_spell_json():
    file_path = resource_path("Data/spells.json")

    def loader():
        return load_json(file_path)
    return get_cache(CACHE_SPELLS, loader)


class SpellLotteryGenerator(Generator):
    """Generate random spells using d9 roll for level, then dX for spell within level"""
    CACHE_KEY = 'spell_lottery'
    DATA_FILE = "Data/spells.json"

    def load(self):
        return load_spell_json()

    def validate_data(self, data: Any) -> None:
        validate_list(data, "Spells")
        for spell in data:
            if not isinstance(spell, dict):
                raise TypeError(f"Invalid spell type: {type(spell)}")
            validate_item(spell, "Spell")

    def generate(self, **kwargs) -> Dict[str, Any]:
        """Required abstract method from Generator base class"""
        return self.generate_random_spell(kwargs.get('class_name'))

    def get_available_levels(self) -> Dict[int, int]:
        """Get spell levels and count of spells at each level"""
        spells = self._get_data()
        levels = {}
        for spell in spells:
            level = spell.get('level', 0)
            levels[level] = levels.get(level, 0) + 1
        return dict(sorted(levels.items()))

    def get_spells_by_level_and_class(self, level: int, class_name: str = None) -> List[Dict[str, Any]]:
        """Get spells filtered by level and optionally by class"""
        spells = self._get_data()
        filtered = []

        for spell in spells:
            if spell.get('level') != level:
                continue

            if class_name:
                classes = [c.lower() for c in spell.get('classes', [])]
                if class_name.lower() not in classes:
                    continue

            filtered.append(spell)

        return filtered

    def generate_random_spell(self, class_name: str = None) -> Dict[str, Any]:
        """
        Generate random spell using d9 roll for level.
        Roll d9 (1-9), then roll dX based on spells available at that level.
        Returns spell with class filter if provided.
        """
        spells = self._get_data()

        # Get available levels
        available_levels = self.get_available_levels()
        if not available_levels:
            raise ValueError("No spells available")

        # Roll d9 to determine spell level (1-9)
        d9_roll = random.randint(1, 9)

        # Map d9 roll to available spell level
        level_list = sorted(available_levels.keys())
        level_index = min(d9_roll - 1, len(level_list) - 1)
        selected_level = level_list[level_index]

        # Get spells at this level
        spells_at_level = self.get_spells_by_level_and_class(
            selected_level, class_name)

        if not spells_at_level:
            # If class filter resulted in no spells, just get all spells at level
            spells_at_level = self.get_spells_by_level_and_class(
                selected_level)

        if not spells_at_level:
            raise ValueError(f"No spells available at level {selected_level}")

        # Roll dX where X is number of spells at this level
        spell_index = random.randint(0, len(spells_at_level) - 1)
        spell = spells_at_level[spell_index]

        return {
            **spell,
            "d9_roll": d9_roll,
            "selected_level": selected_level,
            "spells_count_at_level": len(spells_at_level)
        }


_spell_lottery_instance = SpellLotteryGenerator()


def generate_random_spell(class_name: str = None) -> Dict[str, Any]:
    """Generate random spell with d9 lottery system"""
    return _spell_lottery_instance.generate_random_spell(class_name)


def get_spell_levels_info() -> Dict[int, int]:
    """Get information about spell levels and their counts"""
    return _spell_lottery_instance.get_available_levels()


def generate_spell_for_class(class_name: str) -> Dict[str, Any]:
    """Generate spell specifically for a given class"""
    return _spell_lottery_instance.generate_random_spell(class_name)


def search_spells(name_filter="", level_filter="", class_filter=""):
    """Search spells with filters"""
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
