import random
from logic.core.pathing import resource_path
from logic.core.cache import get_cache
from logic.core.io import load_json
from typing import Dict, Any
from logic.core.generator_base import Generator
from logic.core.empty_validation_check import validate_list, validate_item


class MagicItemsGenerator(Generator):
    CACHE_KEY = 'magic_items'
    DATA_FILE = "Data/magic_items.json"

    def load(self):
        load_json_path = resource_path(self.DATA_FILE)
        return get_cache(self.CACHE_KEY, lambda: load_json(load_json_path))

    def validate_data(self, data: Any) -> None:
        validate_list(data, "Magic items")
        for item in data:
            if not isinstance(item, dict):
                raise TypeError(f"Invalid magic item type: {type(item)}")
            validate_item(item, "Magic item")

    def generate(self, **kwargs) -> Dict[str, Any]:
        items_list = self._get_data()
        item = random.choice(items_list)

        if item is None:
            raise ValueError(
                "Magic item is None (bad data in magic_items.json)")

        return item


_magic_items_generator_instance = MagicItemsGenerator()


def generate_magic_items() -> Dict[str, Any]:
    return _magic_items_generator_instance.generate()
