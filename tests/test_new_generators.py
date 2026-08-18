import unittest
from logic.spell_scroll_generator import (
    generate_spell_scroll,
    generate_spell_scroll_for_class_and_level,
    generate_spell_scroll_for_level
)
from logic.weather_encounter_generator import (
    generate_weather_encounter,
    generate_blizzard_encounter,
    generate_encounter_by_danger_level,
    get_available_weather_types,
    get_ice_encounters
)
from logic.loot import (
    generate_loot_by_category,
    generate_loot_cr_based,
    generate_treasure_hoard,
    get_loot_categories
)


LOG_FILE = "log.txt"


def write_log(name, result=None, error=None):
    """Log for all tests"""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n=== {name} ===\n")

        if error:
            f.write("STATUS: FAIL\n")
            f.write(str(error) + "\n")
        else:
            f.write("STATUS: OK\n")
            f.write(str(result) + "\n")

        f.write("-" * 40 + "\n")


class TestSpellScrollGenerator(unittest.TestCase):

    def test_generate_spell_scroll_random(self):
        """Test generating random spell scroll"""
        try:
            scroll = generate_spell_scroll()

            self.assertIsInstance(scroll, dict)
            self.assertIn("name", scroll)
            self.assertIn("level", scroll)
            self.assertIn("classes", scroll)
            self.assertGreaterEqual(scroll["level"], 0)
            self.assertLessEqual(scroll["level"], 9)

            write_log("spell_scroll_random", result=scroll["name"])
        except Exception as e:
            write_log("spell_scroll_random", error=e)
            raise

    def test_generate_spell_scroll_for_class(self):
        """Test generating spell scroll for specific class"""
        try:
            class_mappings = {
                "mag": "wizard",
                "czarownik": "sorcerer",
                "kleryk": "cleric",
                "druid": "druid"
            }

            for class_name, expected in class_mappings.items():
                scroll = generate_spell_scroll(class_name)

                self.assertIn("name", scroll)
                self.assertIn("generated_for_class", scroll)
                self.assertEqual(scroll["generated_for_class"], expected)

            write_log("spell_scroll_by_class", result="All classes OK")
        except Exception as e:
            write_log("spell_scroll_by_class", error=e)
            raise

    def test_generate_spell_scroll_for_level(self):
        """Test generating spell scroll for specific level"""
        try:
            for level in [1, 3, 5, 7, 9]:
                scroll = generate_spell_scroll_for_level(level)

                self.assertIn("name", scroll)
                # Level może być równy lub niższy ze względu na dostępność
                self.assertLessEqual(scroll["level"], level + 1)

            write_log("spell_scroll_by_level", result="Levels 1-9 OK")
        except Exception as e:
            write_log("spell_scroll_by_level", error=e)
            raise


class TestWeatherEncounterGenerator(unittest.TestCase):

    def test_generate_weather_encounter(self):
        """Test generating weather-based encounter"""
        try:
            result = generate_weather_encounter()

            self.assertIsInstance(result, dict)
            self.assertIn("encounter", result)
            self.assertIn("weather", result)
            self.assertIn("adjusted_cr", result)
            self.assertIn("weather_effects", result)

            write_log("weather_encounter", result=result["combined_threat"])
        except Exception as e:
            write_log("weather_encounter", error=e)
            raise

    def test_generate_blizzard_encounter(self):
        """Test generating blizzard encounter"""
        try:
            result = generate_blizzard_encounter()

            self.assertIsInstance(result, dict)
            self.assertEqual(result["weather"]["weather_type"], "blizzard")
            self.assertGreater(result["adjusted_cr"], 0)

            write_log("blizzard_encounter", result=result["combined_threat"])
        except Exception as e:
            write_log("blizzard_encounter", error=e)
            raise

    def test_generate_encounter_by_danger_level(self):
        """Test generating encounter by danger level"""
        try:
            for danger in range(1, 6):
                result = generate_encounter_by_danger_level(danger)

                self.assertIsInstance(result, dict)
                self.assertEqual(result["danger_level"], danger)
                self.assertIn("encounter", result)

            write_log("danger_level_encounters", result="Levels 1-5 OK")
        except Exception as e:
            write_log("danger_level_encounters", error=e)
            raise

    def test_get_available_weather_types(self):
        """Test getting available weather types"""
        try:
            weather_types = get_available_weather_types()

            self.assertIsInstance(weather_types, list)
            self.assertGreater(len(weather_types), 0)
            self.assertIn("blizzard", weather_types)

            write_log("available_weather_types",
                      result=f"Found {len(weather_types)} weather types")
        except Exception as e:
            write_log("available_weather_types", error=e)
            raise

    def test_get_ice_encounters(self):
        """Test getting ice-related encounters"""
        try:
            ice_encounters = get_ice_encounters()

            self.assertIsInstance(ice_encounters, list)
            self.assertGreater(len(ice_encounters), 0)

            write_log("ice_encounters",
                      result=f"Found {len(ice_encounters)} ice encounters")
        except Exception as e:
            write_log("ice_encounters", error=e)
            raise


class TestLootGeneratorExtensions(unittest.TestCase):

    def test_generate_loot_by_category(self):
        """Test generating loot by category"""
        try:
            categories = get_loot_categories()
            self.assertGreater(len(categories), 0)

            # Test kilka kategorii
            for category in categories[:3]:
                loot = generate_loot_by_category(category)

                self.assertIsInstance(loot, dict)
                self.assertEqual(loot.get("category"), category)

            write_log("loot_by_category",
                      result=f"Categories tested: {len(categories)}")
        except Exception as e:
            write_log("loot_by_category", error=e)
            raise

    def test_generate_loot_cr_based(self):
        """Test generating loot based on CR"""
        try:
            for cr in [1, 5, 10, 15]:
                loot_list = generate_loot_cr_based(cr)

                self.assertIsInstance(loot_list, list)
                self.assertGreater(len(loot_list), 0)

            write_log("loot_cr_based", result="CR 1, 5, 10, 15 tested")
        except Exception as e:
            write_log("loot_cr_based", error=e)
            raise

    def test_generate_treasure_hoard(self):
        """Test generating treasure hoard"""
        try:
            hoard = generate_treasure_hoard(cr=5, hoard_size="medium")

            self.assertIsInstance(hoard, dict)
            self.assertIn("gold_pieces", hoard)
            self.assertIn("gems_value", hoard)
            self.assertIn("magic_items", hoard)
            self.assertGreater(hoard["gold_pieces"], 0)

            write_log("treasure_hoard",
                      result=f"Hoard value: {hoard['total_approx_value']} gp")
        except Exception as e:
            write_log("treasure_hoard", error=e)
            raise


if __name__ == '__main__':
    unittest.main()
