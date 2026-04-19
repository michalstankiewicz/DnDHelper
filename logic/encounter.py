import random
from typing import Dict, Any
from logic.core.generator_base import Generator
from logic.core.pathing import resource_path
from logic.core.cache import get_cache
from logic.core.io import load_json


class EncounterGenerator(Generator):
    """Generate either a monster encounter or an adventure.
    Encounters and adventures are stored in separate JSON files, so the generator handles both sources."""
    CACHE_KEY = "encounter"
    DATA_FILE = "Data/encounter.json"

    ADVENTURE_FILE = "Data/adv.json"

    def load(self):
        """Lazy initialization of encounter"""
        file_path = resource_path(self.DATA_FILE)

        def loader():
            return load_json(file_path)
        return get_cache(self.CACHE_KEY, loader)

    def load_adventures(self):
        """Lazy initialization of adventure"""
        file_path = resource_path(self.ADVENTURE_FILE)

        def loader():
            return load_json(file_path)

        return get_cache("adventures", loader)

    def validate_data(self, data: Any) -> None:
        """Check if encounter.json is a list of encounters"""
        if not isinstance(data, list):
            raise ValueError("Encounters must be a list")
        if len(data) == 0:
            raise ValueError("Encounters list is empty")

    def validate_adventures(self, data: Any) -> None:
        """Check if adventure.json is a list of adventures"""
        if not isinstance(data, list):
            raise ValueError("Adventures must be a list")
        if len(data) == 0:
            raise ValueError("Adventures list is empty")

    def generate(self, **kwargs) -> Dict[str, Any]:
        """Generate list of encounter/adventure from the list"""
        choice_type = random.choices(
            ["monster", "adventure"],
            weights=[0.6, 0.4],
            k=1
        )[0]

        if choice_type == "monster":
            encounters = self.load()
            self.validate_data(encounters)

            data = random.choice(encounters)

            if not isinstance(data, dict):
                raise ValueError("Invalid encounter format")

            result = data.copy()
            result["is_monster"] = True
            return result

        adventures = self.load_adventures()
        self.validate_adventures(adventures)

        data = random.choice(adventures)

        if not isinstance(data, dict):
            raise ValueError("Invalid adventure format")

        result = data.copy()
        result["is_monster"] = False
        return result


_encounter_generator = EncounterGenerator()


def generate_encounter():
    return _encounter_generator.generate()
