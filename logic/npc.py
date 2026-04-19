from logic.core.pathing import resource_path
from logic.core.cache import get_cache
from logic.core.io import load_json
from logic.core.empty_validation_check import validate_item, validate_list
from typing import Dict, Any
from logic.core.generator_base import Generator
import random


class NPCGenerator(Generator):
    CACHE_KEY = "npc"
    DATA_FILE = "Data/npc.json"

    def load(self):
        load_json_path = resource_path(self.DATA_FILE)
        return get_cache(self.CACHE_KEY, lambda: load_json(load_json_path))

    def validate_data(self, data: Any) -> None:
        """Check if json with npc data is loaded correctly"""
        if not isinstance(data, dict):
            raise ValueError(f"Invalid value, expected dict")
        if "races" not in data:
            raise ValueError(f"Missing 'races' in npc data")

    def generate(self, **kwargs) -> Dict[str, Any]:
        data = self.load()
        self.validate_data(data)

        races = data["races"]
        race = random.choice(list(races))

        gender = random.choice(["male", "female"])
        names = races.get(race, {}).get(gender, [])
        validate_list(names, f"Missing names for {race}/{gender}")
        validate_list(data["surnames"], "surnames")
        validate_list(data["traits"], "traits")
        validate_list(data["hooks"], "hooks")
        name = random.choice(names)
        surname = random.choice(data["surnames"])
        trait = random.choice(data["traits"])
        hook = random.choice(data["hooks"])
        return {
            "race": race,
            "gender": gender,
            "name": name,
            "surname": surname,
            "trait": trait,
            "hook": hook
        }


_npc_generate_instance = NPCGenerator()


def generate_npc() -> Dict[str, Any]:
    """Generate random npc"""
    return _npc_generate_instance.generate()
