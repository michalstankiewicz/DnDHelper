import random
from logic.core.pathing import resource_path
from logic.core.cache import get_cache
from logic.core.io import load_json
from typing import Dict, Any, List, Optional
from logic.core.generator_base import Generator
from logic.core.empty_validation_check import validate_list, validate_item


class WeatherEncounterGenerator(Generator):
    """Generator encounter bazowanych na warunkach pogodowych (zwłaszcza zimowych)

    Łączy weather z encounter w realistyczne scenariusze:
    - Burzliwą pogodę z agresywnymi stworzeniami
    - Lód z elementalami i lodowymi istotami
    - Wymieszane efekty środowiskowe
    """

    CACHE_KEY = 'weather_encounters'
    WEATHER_FILE = "Data/weather.json"
    ENCOUNTER_FILE = "Data/encounter.json"

    def load(self):
        weather_path = resource_path(self.WEATHER_FILE)
        encounter_path = resource_path(self.ENCOUNTER_FILE)

        weather_data = get_cache(
            f"{self.CACHE_KEY}_weather", lambda: load_json(weather_path))
        encounter_data = get_cache(
            f"{self.CACHE_KEY}_encounters", lambda: load_json(encounter_path))

        return {
            "weather": weather_data,
            "encounters": encounter_data
        }

    def validate_data(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError("Expected dict with weather and encounters keys")
        validate_list(data.get("weather", []), "Weather data")
        validate_list(data.get("encounters", []), "Encounter data")

    def generate(self, **kwargs) -> Dict[str, Any]:
        """Generuje encounter bazowany na losowej pogodzie"""
        data = self._get_data()
        return self.generate_for_weather(None, **kwargs)

    def generate_for_weather(self, weather_type: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Generuje encounter dla konkretnego typu pogody

        Args:
            weather_type: Typ pogody (blizzard, heavy_snow, ice_storm, etc.)

        Returns:
            Dict z encounter i powiązaną pogodą
        """
        data = self._get_data()
        weather_list = data["weather"]
        encounter_list = data["encounters"]

        # Wybierz pogodę
        if weather_type:
            weather = next(
                (w for w in weather_list if w.get("weather_type") == weather_type),
                None
            )
            if not weather:
                raise ValueError(f"Weather type not found: {weather_type}")
        else:
            weather = random.choice(weather_list)

        # Wzmocnienie zagrożenia na podstawie pogody
        encounter_modifier = weather.get("encounter_modifier", 1.0)
        loot_penalty = weather.get("loot_penalty", 1.0)

        # Filtruj encounter na podstawie intensywności pogody
        intensity = weather.get("intensity", "moderate")
        intensity_weights = {
            "light": lambda enc: enc.get("cr", 0) <= 2,
            "moderate": lambda enc: enc.get("cr", 0) <= 5,
            "heavy": lambda enc: enc.get("cr", 0) <= 8,
            "severe": lambda enc: True,  # Każdy encounter jest możliwy
            "extreme": lambda enc: enc.get("cr", 0) >= 5,
        }

        filter_func = intensity_weights.get(intensity, lambda x: True)
        filtered_encounters = [e for e in encounter_list if filter_func(e)]

        if not filtered_encounters:
            filtered_encounters = encounter_list

        encounter = random.choice(filtered_encounters)

        # Dostosuj trudność na podstawie pogody
        adjusted_cr = encounter.get("cr", 0) * encounter_modifier

        return {
            "encounter": encounter,
            "adjusted_cr": adjusted_cr,
            "weather": weather,
            "weather_effects": weather.get("effects", []),
            "difficulty_modifier": encounter_modifier,
            "loot_penalty": loot_penalty,
            "travel_speed_modifier": weather.get("travel_speed_modifier", 1.0),
            "visibility": weather.get("visibility", 1.0),
            "temperature": weather.get("temperature", 0),
            "description": f"During {weather.get('description', 'weather')}, you encounter {encounter.get('description', 'a creature')}",
            "combined_threat": f"{encounter.get('name')} (CR {adjusted_cr:.1f}) in {weather.get('weather_type')} (intensity: {intensity})"
        }

    def get_weather_types(self) -> List[str]:
        """Zwraca dostępne typy pogody"""
        data = self._get_data()
        return [w.get("weather_type") for w in data["weather"] if w.get("weather_type")]

    def get_ice_encounters(self) -> List[Dict[str, Any]]:
        """Zwraca listę encounter powiązanych z lodem i zimą"""
        data = self._get_data()
        ice_keywords = ["ice", "frost", "frozen",
                        "snow", "yeti", "golem", "elemental", "cold"]

        return [
            e for e in data["encounters"]
            if any(kw in e.get("name", "").lower() or kw in e.get("description", "").lower() for kw in ice_keywords)
        ]

    def generate_blizzard_encounter(self, **kwargs) -> Dict[str, Any]:
        """Specjalny generator dla burz śnieżnych (extreme encounter)"""
        return self.generate_for_weather("blizzard", **kwargs)

    def generate_whiteout_encounter(self, **kwargs) -> Dict[str, Any]:
        """Specjalny generator dla white-out warunków (highest difficulty)"""
        return self.generate_for_weather("whiteout", **kwargs)

    def generate_ice_storm_encounter(self, **kwargs) -> Dict[str, Any]:
        """Specjalny generator dla lodowych burz"""
        return self.generate_for_weather("ice_storm", **kwargs)

    def generate_by_danger_level(self, danger_level: int) -> Dict[str, Any]:
        """Generuje encounter na podstawie poziomu zagrożenia (1-5)

        Args:
            danger_level: 1 (safe) to 5 (deadly)
        """
        data = self._get_data()
        weather_list = data["weather"]
        encounter_list = data["encounters"]

        # Mapuj danger level na intensywność pogody
        danger_to_intensity = {
            1: ["light", "cold_clear"],
            2: ["moderate", "frost", "sleet"],
            3: ["heavy", "heavy_snow", "frozen_fog"],
            4: ["severe", "ice_storm", "blizzard"],
            5: ["extreme", "whiteout", "wind_chill"]
        }

        intensity_options = danger_to_intensity.get(
            max(1, min(5, danger_level)), ["moderate"])
        weather = next(
            (w for w in weather_list if w.get("intensity") in intensity_options),
            random.choice(weather_list)
        )

        # Dostosuj encounter do poziomu zagrożenia
        cr_range = {
            1: (0, 2),
            2: (2, 4),
            3: (4, 8),
            4: (8, 12),
            5: (12, 25)
        }

        min_cr, max_cr = cr_range.get(danger_level, (0, 5))
        filtered_encounters = [
            e for e in encounter_list
            if min_cr <= e.get("cr", 0) <= max_cr
        ]

        if not filtered_encounters:
            filtered_encounters = encounter_list

        encounter = random.choice(filtered_encounters)
        encounter_modifier = weather.get("encounter_modifier", 1.0)

        return {
            "encounter": encounter,
            "weather": weather,
            "danger_level": danger_level,
            "adjusted_cr": encounter.get("cr", 0) * encounter_modifier,
            "description": f"Danger Level {danger_level}: {encounter.get('name')} in {weather.get('weather_type')}"
        }


# Instancja globalna
_weather_encounter_generator_instance = WeatherEncounterGenerator()


def generate_weather_encounter(weather_type: Optional[str] = None) -> Dict[str, Any]:
    """Publiczna funkcja do generowania encounter bazowanego na pogodzie"""
    return _weather_encounter_generator_instance.generate_for_weather(weather_type)


def generate_blizzard_encounter() -> Dict[str, Any]:
    """Generuje encounter podczas burzy śnieżnej"""
    return _weather_encounter_generator_instance.generate_blizzard_encounter()


def generate_whiteout_encounter() -> Dict[str, Any]:
    """Generuje encounter podczas white-out warunków"""
    return _weather_encounter_generator_instance.generate_whiteout_encounter()


def generate_ice_storm_encounter() -> Dict[str, Any]:
    """Generuje encounter podczas lodowej burzy"""
    return _weather_encounter_generator_instance.generate_ice_storm_encounter()


def generate_encounter_by_danger_level(danger_level: int) -> Dict[str, Any]:
    """Generuje encounter na podstawie poziomu zagrożenia (1-5)"""
    return _weather_encounter_generator_instance.generate_by_danger_level(danger_level)


def get_available_weather_types() -> List[str]:
    """Zwraca dostępne typy pogody"""
    return _weather_encounter_generator_instance.get_weather_types()


def get_ice_encounters() -> List[Dict[str, Any]]:
    """Zwraca listę encounter powiązanych z lodem"""
    return _weather_encounter_generator_instance.get_ice_encounters()
