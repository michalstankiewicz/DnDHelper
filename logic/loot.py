import random
from logic.core.pathing import resource_path
from logic.core.cache import get_cache
from logic.core.io import load_json
from typing import Dict, Any, List, Optional
from logic.core.generator_base import Generator
from logic.core.empty_validation_check import validate_list, validate_item


class LootGenerator(Generator):
    CACHE_KEY = 'loot'
    DATA_FILE = "Data/loot.json"

    def load(self):
        load_json_path = resource_path(self.DATA_FILE)
        return get_cache(self.CACHE_KEY, lambda: load_json(load_json_path))

    def validate_data(self, data: Any) -> None:
        validate_list(data, "Loot")
        for item in data:
            if not isinstance(item, dict):
                raise TypeError(f"Invalid loot item type: {type(item)}")
            validate_item(item, "Loot item")

    def generate(self, **kwargs) -> Dict[str, Any]:
        loot_list = self._get_data()
        item = random.choice(loot_list)

        if item is None:
            raise ValueError("Loot item is None (bad data in loot.json)")

        return item

    def generate_multiple(self, count: int = 3) -> List[Dict[str, Any]]:
        """Generate multiple loot items without duplicates"""
        loot_list = self._get_data()
        if count > len(loot_list):
            count = len(loot_list)

        return random.sample(loot_list, count)

    def generate_by_rarity(self, rarity: str = None) -> Dict[str, Any]:
        """Generate loot filtered by rarity (common, uncommon, rare, very_rare, legendary)"""
        loot_list = self._get_data()

        if rarity:
            filtered = [item for item in loot_list if item.get(
                'rarity', '').lower() == rarity.lower()]
            if filtered:
                return random.choice(filtered)

        return random.choice(loot_list)

    def get_available_rarities(self) -> List[str]:
        """Get list of available rarity levels"""
        loot_list = self._get_data()
        rarities = set()
        for item in loot_list:
            rarity = item.get('rarity')
            if rarity:
                rarities.add(rarity.lower())
        return sorted(list(rarities))

    def get_available_categories(self) -> List[str]:
        """Get list of available item categories"""
        loot_list = self._get_data()
        categories = set()
        for item in loot_list:
            category = item.get('category')
            if category:
                categories.add(category)
        return sorted(list(categories))

    def get_available_types(self) -> List[str]:
        """Get list of available item types"""
        loot_list = self._get_data()
        types = set()
        for item in loot_list:
            item_type = item.get('type')
            if item_type:
                types.add(item_type)
        return sorted(list(types))

    def generate_by_category(self, category: str) -> Dict[str, Any]:
        """Generate loot filtered by category (bronie, pancerze, magiczne_bronie, etc.)"""
        loot_list = self._get_data()
        filtered = [item for item in loot_list if item.get(
            'category', '').lower() == category.lower()]
        if filtered:
            return random.choice(filtered)
        else:
            raise ValueError(f"Brak przedmiotów w kategorii: {category}")

    def generate_by_type(self, item_type: str) -> Dict[str, Any]:
        """Generate loot filtered by type (weapon, armor, magical_item, scroll, potion, etc.)"""
        loot_list = self._get_data()
        filtered = [item for item in loot_list if item.get(
            'type', '').lower() == item_type.lower()]
        if filtered:
            return random.choice(filtered)
        else:
            raise ValueError(f"Brak przedmiotów typu: {item_type}")

    def generate_by_category_and_rarity(self, category: str, rarity: str) -> Dict[str, Any]:
        """Generate loot filtered by both category and rarity"""
        loot_list = self._get_data()
        filtered = [
            item for item in loot_list
            if item.get('category', '').lower() == category.lower() and
            item.get('rarity', '').lower() == rarity.lower()
        ]
        if filtered:
            return random.choice(filtered)
        else:
            raise ValueError(
                f"Brak przedmiotów w kategorii {category} z rzadkością {rarity}")

    def generate_cr_based_loot(self, cr: float) -> List[Dict[str, Any]]:
        """Generuje skarb bazowany na Challenge Rating (CR) z Dungeon Master's Guide

        Tabela przybliżona:
        - CR 0-1: 1-2 common/uncommon items
        - CR 2-4: 2-3 uncommon items
        - CR 5-8: 2-3 rare items
        - CR 9-12: 2-4 rare items
        - CR 13+: 2-3 very_rare/legendary items
        """
        if cr <= 1:
            count = random.randint(1, 2)
            rarities = ["common", "uncommon"]
        elif cr <= 4:
            count = random.randint(2, 3)
            rarities = ["uncommon"]
        elif cr <= 8:
            count = random.randint(2, 3)
            rarities = ["rare"]
        elif cr <= 12:
            count = random.randint(2, 4)
            rarities = ["rare"]
        else:  # CR 13+
            count = random.randint(2, 3)
            rarities = ["very_rare", "legendary"]

        loot = []
        for _ in range(count):
            rarity = random.choice(rarities)
            try:
                item = self.generate_by_rarity(rarity)
                loot.append(item)
            except:
                # Jeśli nie ma przedmiotu z tą rzadkością, spróbuj domyślnie
                item = self.generate()
                loot.append(item)

        return loot

    def generate_treasure_hoard(self, cr: float, hoard_size: str = "medium") -> Dict[str, Any]:
        """Generuje pełny skarb (hoard) zgodnie z Dungeon Master's Guide

        Args:
            cr: Challenge Rating przeciwnika/przeszkody
            hoard_size: "small", "medium", "large" (rozmiar skarbca)

        Returns:
            Dict zawierający: gold (monety), gems (klejnoty), magic_items (przedmioty magiczne)
        """
        # Przybliżone wartości z DMG
        hoard_configs = {
            "small": {
                "gold_dice": "2d6",
                "gem_count": random.randint(0, 2),
                "magic_item_count": random.randint(0, 1)
            },
            "medium": {
                "gold_dice": "4d6",
                "gem_count": random.randint(1, 3),
                "magic_item_count": random.randint(1, 2)
            },
            "large": {
                "gold_dice": "8d6",
                "gem_count": random.randint(2, 5),
                "magic_item_count": random.randint(2, 4)
            }
        }

        config = hoard_configs.get(hoard_size.lower(), hoard_configs["medium"])

        # Losuj złoto
        gold = sum(random.randint(1, 6)
                   for _ in range(int(config["gold_dice"].split("d")[0]))) * 100

        # Generuj klejnoty (po prostu jako wartość)
        gems = config["gem_count"] * random.randint(10, 50)

        # Generuj przedmioty magiczne bazowane na CR
        magic_items = self.generate_cr_based_loot(cr)

        return {
            "gold_pieces": gold,
            "gems_value": gems,
            "magic_items": magic_items,
            "total_approx_value": gold + gems + sum(item.get('value', 0) for item in magic_items),
            "hoard_size": hoard_size,
            "cr": cr
        }


_loot_generator_instance = LootGenerator()


def generate_loot() -> Dict[str, Any]:
    """Generate single random loot item"""
    return _loot_generator_instance.generate()


def generate_loot_multiple(count: int = 3) -> List[Dict[str, Any]]:
    """Generate multiple loot items without duplicates"""
    return _loot_generator_instance.generate_multiple(count)


def generate_loot_by_rarity(rarity: str) -> Dict[str, Any]:
    """Generate loot filtered by specific rarity"""
    return _loot_generator_instance.generate_by_rarity(rarity)


def get_loot_rarities() -> List[str]:
    """Get available rarity levels"""
    return _loot_generator_instance.get_available_rarities()


def get_loot_categories() -> List[str]:
    """Get available item categories"""
    return _loot_generator_instance.get_available_categories()


def get_loot_types() -> List[str]:
    """Get available item types"""
    return _loot_generator_instance.get_available_types()


def generate_loot_by_category(category: str) -> Dict[str, Any]:
    """Generate loot from specific category"""
    return _loot_generator_instance.generate_by_category(category)


def generate_loot_by_type(item_type: str) -> Dict[str, Any]:
    """Generate loot from specific type"""
    return _loot_generator_instance.generate_by_type(item_type)


def generate_loot_by_category_and_rarity(category: str, rarity: str) -> Dict[str, Any]:
    """Generate loot from specific category and rarity"""
    return _loot_generator_instance.generate_by_category_and_rarity(category, rarity)


def generate_loot_cr_based(cr: float) -> List[Dict[str, Any]]:
    """Generate loot based on Challenge Rating"""
    return _loot_generator_instance.generate_cr_based_loot(cr)


def generate_treasure_hoard(cr: float, hoard_size: str = "medium") -> Dict[str, Any]:
    """Generate complete treasure hoard"""
    return _loot_generator_instance.generate_treasure_hoard(cr, hoard_size)
