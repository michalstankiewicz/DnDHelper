import random
from logic.core.pathing import resource_path
from logic.core.cache import get_cache
from logic.core.io import load_json
from logic.core.empty_validation_check import validate_item, validate_list
from logic.core.generator_base import Generator
from typing import Dict, Any, List, Optional


CACHE_SPELLS = "spells"


def load_spell_json():
    file_path = resource_path("Data/spells.json")

    def loader():
        return load_json(file_path)

    return get_cache(CACHE_SPELLS, loader)


class SpellScrollGenerator(Generator):
    """Generator zaklęć i zwojów dla różnych klas D&D

    Obsługuje:
    - Mag (Wizard)
    - Czarownik (Sorcerer)
    - Kleryk (Cleric)
    - Druid (Druid)
    - Bard (Bard)
    - Czarnoksiężnik (Warlock)

    Algorytm: rzut k9 na poziom (1-9), następnie dX gdzie X = liczba zaklęć na tym poziomie
    """

    CACHE_KEY = 'spell_scrolls'
    DATA_FILE = "Data/spells.json"

    # Mapowanie nazw klas na angielskie identyfikatory
    CLASS_MAPPING = {
        "mag": "wizard",
        "czarownik": "sorcerer",
        "kleryk": "cleric",
        "druid": "druid",
        "bard": "bard",
        "czarnoksiężnik": "warlock",
        # Angielskie wersje
        "wizard": "wizard",
        "sorcerer": "sorcerer",
        "cleric": "cleric",
        "druid": "druid",
        "bard": "bard",
        "warlock": "warlock",
    }

    def load(self):
        return load_spell_json()

    def validate_data(self, data: Any) -> None:
        validate_list(data, "Spells")
        for spell in data:
            if not isinstance(spell, dict):
                raise TypeError(f"Invalid spell type: {type(spell)}")
            validate_item(spell, "Spell")

    def generate(self, **kwargs) -> Dict[str, Any]:
        """Generuje pojedynczy zwój zaklęcia dla losowej klasy"""
        spell_class = random.choice(list(self.CLASS_MAPPING.keys())[:6])
        return self.generate_for_class(spell_class, **kwargs)

    def get_available_levels(self) -> Dict[int, int]:
        """Zwraca dostępne poziomy zaklęć i ich liczbę"""
        spells = self._get_data()
        levels = {}
        for spell in spells:
            level = spell.get('level', 0)
            levels[level] = levels.get(level, 0) + 1
        return dict(sorted(levels.items()))

    def get_spells_by_level_and_class(self, level: int, class_name: str = None) -> List[Dict[str, Any]]:
        """Zwraca zaklęcia filtrowane po poziomie i opcjonalnie po klasie"""
        spells = self._get_data()
        class_name_normalized = self.CLASS_MAPPING.get(
            class_name.lower(), class_name.lower()) if class_name else None

        filtered = []
        for spell in spells:
            spell_level = spell.get('level', 0)
            if spell_level != level:
                continue

            if class_name_normalized:
                classes = spell.get('classes', [])
                if class_name_normalized not in [c.lower() for c in classes]:
                    continue

            filtered.append(spell)

        return filtered

    def generate_for_class(self, class_name: str, specific_level: Optional[int] = None) -> Dict[str, Any]:
        """Generuje zwój zaklęcia dla konkretnej klasy

        Args:
            class_name: Nazwa klasy (mag, czarownik, kleryk, druid, bard, czarnoksiężnik)
            specific_level: Opcjonalnie konkretny poziom zaklęcia (0-9)

        Returns:
            Dict zawierający zaklęcie i metadane
        """
        spells = self._get_data()
        class_name_normalized = self.CLASS_MAPPING.get(
            class_name.lower(), class_name.lower())

        # Filtruj zaklęcia dostępne dla klasy
        available_spells = [
            spell for spell in spells
            if class_name_normalized.lower() in [c.lower() for c in spell.get('classes', [])]
        ]

        if not available_spells:
            raise ValueError(f"Brak dostępnych zaklęć dla klasy: {class_name}")

        # Jeśli podano konkretny poziom, użyj go
        if specific_level is not None:
            spells_at_level = [s for s in available_spells if s.get(
                'level', 0) == specific_level]
            if not spells_at_level:
                raise ValueError(
                    f"Brak zaklęć poziomu {specific_level} dla klasy {class_name}")
            spell = random.choice(spells_at_level)
        else:
            # Rzut k9 na poziom zaklęcia (1-9)
            spell_level_roll = random.randint(1, 9)

            # Dostosuj poziom jeśli to warlock (max 5)
            if class_name_normalized.lower() == "warlock":
                spell_level_roll = min(spell_level_roll, 5)

            # Filtruj zaklęcia na danym poziomie
            spells_at_level = [s for s in available_spells if s.get(
                'level', 0) == spell_level_roll]

            # Jeśli brak zaklęć na tym poziomie, spróbuj niżej
            while not spells_at_level and spell_level_roll > 0:
                spell_level_roll -= 1
                spells_at_level = [s for s in available_spells if s.get(
                    'level', 0) == spell_level_roll]

            if not spells_at_level:
                raise ValueError(
                    f"Brak dostępnych zaklęć dla klasy {class_name}")

            # rzut dX gdzie X = liczba zaklęć na tym poziomie
            spell = random.choice(spells_at_level)

        return {
            "name": spell.get('name'),
            "level": spell.get('level', 0),
            "school": spell.get('school', 'unknown'),
            "classes": spell.get('classes', []),
            "description": spell.get('description', ''),
            "range": spell.get('range', 'Unknown'),
            "components": spell.get('components', []),
            "duration": spell.get('duration', ''),
            "concentration": spell.get('concentration', False),
            "ritual": spell.get('ritual', False),
            "type": "spell_scroll",
            "generated_for_class": class_name_normalized
        }

    def generate_for_class_and_level(self, class_name: str, level: int) -> Dict[str, Any]:
        """Generator zaklęcia dla konkretnej klasy i poziomu"""
        return self.generate_for_class(class_name, specific_level=level)

    def generate_with_level_and_spell_roll(self, class_name: str) -> Dict[str, Any]:
        """Generuje zwój zaklęcia dla klasy:

        1) Rzut 1d9 na poziom zaklęcia
        2) Rzut dX gdzie X to liczba dostępnych zaklęć dla tej klasy i levelu
        """
        class_name_normalized = self.CLASS_MAPPING.get(
            class_name.lower(), class_name.lower())

        spell_level_roll = random.randint(1, 9)
        if class_name_normalized.lower() == "warlock":
            spell_level_roll = min(spell_level_roll, 5)

        spells_at_level = self.get_spells_by_level_and_class(
            spell_level_roll, class_name_normalized)
        spells_count = len(spells_at_level)

        if spells_count == 0:
            raise ValueError(
                f"Brak dostępnych zaklęć dla klasy {class_name} na poziomie {spell_level_roll}")

        spell_roll = random.randint(1, spells_count)
        spell = spells_at_level[spell_roll - 1]

        return {
            "name": spell.get('name'),
            "level": spell.get('level', 0),
            "school": spell.get('school', 'unknown'),
            "classes": spell.get('classes', []),
            "description": spell.get('description', ''),
            "range": spell.get('range', 'Unknown'),
            "components": spell.get('components', []),
            "duration": spell.get('duration', ''),
            "concentration": spell.get('concentration', False),
            "ritual": spell.get('ritual', False),
            "type": "spell_scroll",
            "generated_for_class": class_name_normalized,
            "level_roll": spell_level_roll,
            "spells_count": spells_count,
            "spell_roll": spell_roll,
        }

    def generate_random_spell_by_level(self, level: int) -> Dict[str, Any]:
        """Generuje losowe zaklęcie dla danego poziomu"""
        spells_at_level = self.get_spells_by_level_and_class(level)
        if not spells_at_level:
            raise ValueError(f"Brak zaklęć poziomu {level}")

        spell = random.choice(spells_at_level)
        return {
            "name": spell.get('name'),
            "level": spell.get('level', 0),
            "school": spell.get('school', 'unknown'),
            "classes": spell.get('classes', []),
            "description": spell.get('description', ''),
            "range": spell.get('range', 'Unknown'),
            "components": spell.get('components', []),
            "duration": spell.get('duration', ''),
            "concentration": spell.get('concentration', False),
            "ritual": spell.get('ritual', False),
            "type": "spell_scroll"
        }

    def get_classes_list(self) -> List[str]:
        """Zwraca listę obsługiwanych klas"""
        return list(self.CLASS_MAPPING.keys())[:6]


# Instancja globalna
_spell_scroll_generator_instance = SpellScrollGenerator()


def generate_spell_scroll(class_name: Optional[str] = None) -> Dict[str, Any]:
    """Publiczna funkcja do generowania zwoju zaklęcia

    Args:
        class_name: Nazwa klasy (mag, czarownik, kleryk, druid, bard, czarnoksiężnik) 
                   Jeśli None, wybiera losową klasę

    Returns:
        Dict zawierający zaklęcie w formacie zwoju
    """
    if class_name:
        return _spell_scroll_generator_instance.generate_for_class(class_name)
    else:
        return _spell_scroll_generator_instance.generate()


def generate_spell_scroll_for_level(level: int) -> Dict[str, Any]:
    """Generuje zwój zaklęcia dla konkretnego poziomu"""
    return _spell_scroll_generator_instance.generate_random_spell_by_level(level)


def generate_spell_scroll_for_class_and_level(class_name: str, level: int) -> Dict[str, Any]:
    """Generuje zwój zaklęcia dla konkretnej klasy i poziomu"""
    return _spell_scroll_generator_instance.generate_for_class_and_level(class_name, level)


def generate_spell_scroll_with_rolls(class_name: str) -> Dict[str, Any]:
    """Generuje zwój zaklęcia dla klasy, używając rzutu 1d9 i następnie dX."""
    return _spell_scroll_generator_instance.generate_with_level_and_spell_roll(class_name)
