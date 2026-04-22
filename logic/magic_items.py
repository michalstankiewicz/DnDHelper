import random
from logic.core.generator_base import Generator
from typing import Dict, Any
from logic.core.pathing import resource_path
from logic.core.io import load_json
from logic.core.cache import get_cache
from logic.core.empty_validation_check import validate_list, validate_item


class MagicItemGenerator(Generator):
    CACHE_KEY = 'magic_items'
    DATA_FILE = "Data/magic_items.json"

    def load(self):
        load_json_path = resource_path(self.DATA_FILE)
        return get_cache(self.CACHE_KEY, lambda: load_json(load_json_path))

    def validate_data(self, data: Any) -> None:
        """Check if loot.json is a list of items"""
        validate_list(data, "Magic item")
        for item in data:
            if not isinstance(item, dict):
                raise TypeError(f"Invalid loot item type: {type(item)}")
            validate_item(item, "Magic item")

    def generate(self, **kwargs) -> Dict[str, Any]:
        """Generate random item from loot list"""
        magic_item_list = self._get_data()
        item = random.choice(magic_item_list)

        if item is None:
            raise ValueError(
                "Loot item is None (bad data in magic_items.json)")

        return item


_magic_item_loot_instance = MagicItemGenerator()


def generate_magic_item() -> Dict[str, Any]:
    """Generate Magic item"""
    return _magic_item_loot_instance.generate()
