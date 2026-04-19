import unittest

from logic.city_gen import generate_city
from logic.encounter import generate_encounter
from logic.loot import generate_loot
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

            self.assertEqual(len(result["problems"]), 2)
            self.assertEqual(len(result["goods"]), 2)

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

    def test_generate_encounter(self):
        try:
            result = generate_encounter()

            self.assertIsInstance(result, dict)
            self.assertIn("is_monster", result)

            write_log("encounter", result=result)

        except Exception as e:
            write_log("encounter", error=e)
            raise


class TestLoot(unittest.TestCase):

    def test_generate_loot(self):
        try:
            result = generate_loot()

            self.assertIsInstance(result, dict)

            write_log("loot", result=result)

        except Exception as e:
            write_log("loot", error=e)
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


if __name__ == "__main__":
    # reset log once per run
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("=== TEST RUN START ===\n")

    unittest.main()
