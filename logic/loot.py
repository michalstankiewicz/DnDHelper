import random
from logic.core.pathing import resource_path
from logic.core.cache import get_cache
from logic.core.io import load_json
from typing import Dict, Any
from logic.core.generator_base import Generator
from logic.core.empty_validation_check import validate_list, validate_item


class LootGenerator(Generator):
    """Loot generator to create list of random items"""
    CACHE_KEY = 'loot'
    DATA_FILE = "Data/loot.json"

    def load(self):
        load_json_path = resource_path(self.DATA_FILE)
        return get_cache(self.CACHE_KEY, lambda: load_json(load_json_path))

    def validate_data(self, data: Any) -> None:
        """Check if loot.json is a list of items"""
        validate_list(data, "Loot")
        for item in data:
            if not isinstance(item, dict):
                raise TypeError(f"Invalid loot item type: {type(item)}")
            validate_item(item, "Loot item")

    def generate(self, **kwargs) -> Dict[str, Any]:
        """Generate random item from loot list"""
        loot_list = self._get_data()
        item = random.choice(loot_list)

        if item is None:
            raise ValueError("Loot item is None (bad data in loot.json)")

        return item


_loot_generator_instance = LootGenerator()


def generate_loot() -> Dict[str, Any]:
    """Generate random loot item using singleton instance."""
    return _loot_generator_instance.generate()
