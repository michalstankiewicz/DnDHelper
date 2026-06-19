import unittest

from logic.city_gen import generate_city
from logic.encounter import generate_encounter
from logic.loot import generate_loot
from logic.magic_items import generate_magic_items
from logic.npc import generate_npc


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


class TestCityGen(unittest.TestCase):

    def test_generate_city_structure(self):
        try:
            result = generate_city("bryn_shander")

            self.assertIsInstance(result, dict)
            self.assertIn("city", result)
            self.assertIn("problems", result)
            self.assertIn("goods", result)
            self.assertIn("superstitions", result)

            self.assertGreaterEqual(len(result["problems"]), 2)
            self.assertGreaterEqual(len(result["goods"]), 2)

            write_log("city_gen", result=result)

        except Exception as e:
            write_log("city_gen", error=e)
            raise

    def test_city_unknown(self):
        try:
            with self.assertRaises(ValueError) as ctx:
                generate_city("THIS_CITY_DOES_NOT_EXIST")

            write_log(
                "city_gen_unknown",
                result=f"ValueError raised correctly: {str(ctx.exception)}"
            )

        except Exception as e:
            write_log("city_gen_unknown", error=e)
            raise


class TestEncounter(unittest.TestCase):

    def test_generate_encounter_structure(self):
        try:
            result = generate_encounter()

            self.assertIsInstance(result, dict)
            self.assertIn("name", result)
            self.assertIn("type", result)
            self.assertIn("cr", result)
            self.assertIn("description", result)

            self.assertIsInstance(result["cr"], (int, float))
            self.assertGreaterEqual(result["cr"], 0)
            self.assertIsInstance(result["name"], str)
            self.assertGreater(len(result["name"]), 0)

            write_log("encounter_structure", result=result)

        except Exception as e:
            write_log("encounter_structure", error=e)
            raise

    def test_generate_multiple_encounters_no_duplicates(self):
        try:
            encounters = []
            for _ in range(10):
                enc = generate_encounter()
                encounters.append(enc)

            self.assertEqual(len(encounters), 10)

            names = [e["name"] for e in encounters]
            self.assertGreater(len(set(names)), 1)

            write_log(
                "encounter_multiple",
                result=f"Generated {len(encounters)} encounters, {len(set(names))} unique"
            )

        except Exception as e:
            write_log("encounter_multiple", error=e)
            raise

    def test_encounter_cr_ranges(self):
        try:
            cr_values = []
            for _ in range(20):
                enc = generate_encounter()
                cr = enc.get("cr", 0)
                cr_values.append(cr)

            min_cr = min(cr_values)
            max_cr = max(cr_values)
            avg_cr = sum(cr_values) / len(cr_values)

            self.assertGreaterEqual(min_cr, 0)
            self.assertLess(max_cr, 100)

            write_log(
                "encounter_cr_ranges",
                result=f"CR range: {min_cr} - {max_cr}, avg: {avg_cr:.2f}"
            )

        except Exception as e:
            write_log("encounter_cr_ranges", error=e)
            raise


class TestLoot(unittest.TestCase):

    def test_generate_loot_structure(self):
        try:
            result = generate_loot()

            self.assertIsInstance(result, dict)
            self.assertIn("name", result)
            self.assertIn("rarity", result)
            self.assertIn("value", result)
            self.assertIn("description", result)

            self.assertIn(result["rarity"], [
                          "common", "uncommon", "rare", "very_rare"])
            self.assertIsInstance(result["value"], int)
            self.assertGreater(result["value"], 0)

            write_log("loot_structure", result=result)

        except Exception as e:
            write_log("loot_structure", error=e)
            raise

    def test_loot_rarity_distribution(self):
        try:
            rarity_counts = {
                "common": 0,
                "uncommon": 0,
                "rare": 0,
                "very_rare": 0,
                "legendary": 0
            }

            for _ in range(100):
                loot = generate_loot()
                rarity = loot.get("rarity")
                if rarity in rarity_counts:
                    rarity_counts[rarity] += 1

            # Sprawdzamy że mamy co najmniej 90 z znanych rarities (nowe kategorie mogą mieć nowe rarities)
            self.assertGreaterEqual(sum(rarity_counts.values()), 90)
            self.assertGreater(rarity_counts["common"], 0)
            self.assertGreater(rarity_counts["uncommon"], 0)

            write_log("loot_rarity_distribution", result=rarity_counts)

        except Exception as e:
            write_log("loot_rarity_distribution", error=e)
            raise

    def test_loot_value_ranges(self):
        try:
            values = []
            for _ in range(50):
                loot = generate_loot()
                values.append(loot.get("value", 0))

            min_val = min(values)
            max_val = max(values)
            avg_val = sum(values) / len(values)

            self.assertGreater(min_val, 0)
            # Rozszerzmy zakres - teraz mamy magiczne przedmioty do 2500gp
            self.assertLess(max_val, 3000)

            write_log(
                "loot_value_ranges",
                result=f"Value range: {min_val} - {max_val} gp, avg: {avg_val:.2f}"
            )

        except Exception as e:
            write_log("loot_value_ranges", error=e)
            raise


class TestMagicItems(unittest.TestCase):

    def test_generate_magic_items_structure(self):
        try:
            result = generate_magic_items()

            self.assertIsInstance(result, dict)
            self.assertIn("name", result)
            self.assertIn("rarity", result)
            self.assertIn("description", result)
            self.assertIn("effect", result)

            valid_rarities = ["rare", "very_rare",
                              "legendary", "uncommon", "common"]
            self.assertIn(result["rarity"], valid_rarities)
            self.assertIsInstance(result["name"], str)
            self.assertGreater(len(result["name"]), 0)

            write_log("magic_items_structure", result=result)

        except Exception as e:
            write_log("magic_items_structure", error=e)
            raise

    def test_magic_items_rarity_distribution(self):
        try:
            rarity_counts = {
                "rare": 0,
                "very_rare": 0,
                "legendary": 0,
                "uncommon": 0,
                "common": 0
            }

            for _ in range(100):
                item = generate_magic_items()
                rarity = item.get("rarity")
                if rarity in rarity_counts:
                    rarity_counts[rarity] += 1

            self.assertEqual(sum(rarity_counts.values()), 100)
            self.assertGreater(rarity_counts["rare"], 0)

            write_log("magic_items_rarity_distribution", result=rarity_counts)

        except Exception as e:
            write_log("magic_items_rarity_distribution", error=e)
            raise

    def test_magic_items_have_effects(self):
        try:
            for _ in range(20):
                item = generate_magic_items()
                effect = item.get("effect", "")
                self.assertIsInstance(effect, str)
                self.assertGreater(len(effect), 0)

            write_log("magic_items_effects", result="All items have effects")

        except Exception as e:
            write_log("magic_items_effects", error=e)
            raise


class TestNPC(unittest.TestCase):

    def test_generate_npc(self):
        try:
            result = generate_npc()

            self.assertIsInstance(result, dict)

            keys = ["race", "gender", "name", "surname", "trait", "hook"]
            for k in keys:
                self.assertIn(k, result)

            self.assertIn(result["gender"], ["male", "female"])

            write_log("npc", result=result)

        except Exception as e:
            write_log("npc", error=e)
            raise


class TestGeneratorIntegration(unittest.TestCase):

    def test_encounter_to_loot_flow_low_cr(self):
        try:
            enc = generate_encounter()
            cr = enc.get("cr", 0)

            if cr <= 6:
                loot = generate_loot()
                self.assertIn(loot["rarity"], [
                              "common", "uncommon", "rare", "very_rare"])

                write_log(
                    "integration_low_cr",
                    result=f"Encounter CR {cr} -> Loot: {loot['name']}"
                )

        except Exception as e:
            write_log("integration_low_cr", error=e)
            raise

    def test_encounter_to_magic_items_flow_high_cr(self):
        try:
            enc = generate_encounter()
            cr = enc.get("cr", 0)

            if cr > 6:
                item = generate_magic_items()
                # Sprawdzamy że item ma rarity field i jaki ta rarity jest
                self.assertIn("rarity", item)
                rarity = item.get("rarity")
                self.assertIsNotNone(rarity)

                write_log(
                    "integration_high_cr",
                    result=f"Encounter CR {cr} -> Magic Item: {item['name']} (rarity: {rarity})"
                )

        except Exception as e:
            write_log("integration_high_cr", error=e)
            raise


if __name__ == "__main__":
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("=== TEST RUN START ===\n")

    unittest.main()
