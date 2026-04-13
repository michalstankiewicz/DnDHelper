import json
import os
import random
import sys
# PATH


def resource_path(relative_path):
    """Absolute file path for both dev and exe."""
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS  # PyInstaller
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, relative_path)


# Lazy initalization, cache
_city_cache = None


def get_city_data():
    global _city_cache

    if _city_cache is None:
        file_path = resource_path("Data/city_template.json")
        with open(file_path, encoding="utf-8") as f:
            _city_cache = json.load(f)

    return _city_cache

# Function to generate


def city_gen(city_name):
    """City generator"""
    data = get_city_data()
    assert _city_cache is not None, "Encounter Cache not loaded"
    city = data[city_name]
    problems = random.sample(city["problems"], 2)
    goods = random.sample(city["goods"], 2)
    superstitions = random.sample(city["superstitions"], 1)[0]

    return {
        "city": city_name,
        "problems": problems,
        "superstitions": superstitions,
        "goods": goods
    }
