import random
from logic.core.pathing import resource_path
from logic.core.cache import get_cache
from logic.core.io import load_json
from typing import Dict, Any
from logic.core.generator_base import Generator
from logic.core.empty_validation_check import validate_list, validate_item


class EncounterGenerator(Generator):
    CACHE_KEY = 'encounters'
    DATA_FILE = "Data/encounter.json"

    def load(self):
        load_json_path = resource_path(self.DATA_FILE)
        return get_cache(self.CACHE_KEY, lambda: load_json(load_json_path))

    def validate_data(self, data: Any) -> None:
        validate_list(data, "Encounters")
        for item in data:
            if not isinstance(item, dict):
                raise TypeError(f"Invalid encounter type: {type(item)}")
            validate_item(item, "Encounter")

    def generate(self, **kwargs) -> Dict[str, Any]:
        encounters_list = self._get_data()
        encounter = random.choice(encounters_list)

        if encounter is None:
            raise ValueError("Encounter is None (bad data in encounters.json)")

        return encounter


_encounter_generator_instance = EncounterGenerator()


def generate_encounter() -> Dict[str, Any]:
    return _encounter_generator_instance.generate()
