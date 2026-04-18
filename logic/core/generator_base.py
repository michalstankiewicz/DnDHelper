from abc import ABC, abstractmethod
from typing import Dict, Any, List
import random
from logic.core.cache import get_cache
from logic.core.io import load_json
from logic.core.pathing import resource_path


class Generator(ABC):
    """Class to quickly create new generatros in the future"""
    CACHE_KEY: str
    DATA_FILE: str

    def __init__(self):
        self._data = None

    @abstractmethod
    def validate_data(self, data: Any) -> None:
        """Validate loaded data structure."""
        pass

    @abstractmethod
    def generate(self, **kwargs) -> Dict[str, Any]:
        """Generate random item."""
        pass

    def load(self) -> Any:
        """Load and cache data."""
        file_path = resource_path(self.DATA_FILE)
        return get_cache(self.CACHE_KEY, lambda: load_json(file_path))

    def _get_data(self) -> Any:
        """Lazy load data with validation."""
        if self._data is None:
            self._data = self.load()
            self.validate_data(self._data)
        return self._data
