import unittest
from dice import roll_dice, roll_multiple_dice, roll_from_string


class TestDiceFunctions(unittest.TestCase):

    def test_roll_dice(self):
        for sides in [4, 6, 8, 10, 12, 20]:
            result = roll_dice(sides)
            self.assertTrue(1 <= result <= sides,
                            f"Result {result} is out of bounds for d{sides}")

    def test_roll_multiple_dice(self):
        rolls, total = roll_multiple_dice(3, 6)
        self.assertEqual(len(rolls), 3, "Should roll exactly 3 dice")
        self.assertTrue(all(1 <= roll <= 6 for roll in rolls),
                        "Each roll should be between 1 and 6")
        self.assertEqual(total, sum(rolls), "Total should be the sum of rolls")

    def test_roll_from_string(self):
        rolls, total = roll_from_string("2d8")
        self.assertEqual(len(rolls), 2, "Should roll exactly 2 dice")
        self.assertTrue(all(1 <= roll <= 8 for roll in rolls),
                        "Each roll should be between 1 and 8")
        self.assertEqual(total, sum(rolls), "Total should be the sum of rolls")

        with self.assertRaises(ValueError):
            roll_from_string("invalid")
        with self.assertRaises(ValueError):
            roll_from_string("2d")

    def test_roll_multiple_dice_invalid(self):
        with self.assertRaises(ValueError):
            roll_multiple_dice(0, 6)
