import unittest
from pyssq.doublecolor import DoubleColorBall


class TestDoubleColorBall(unittest.TestCase):
    def test_generate(self):
        result = DoubleColorBall.generate()
        self.assertIn("red", result)
        self.assertIn("blue", result)
        self.assertEqual(len(result["red"]), 6)
        self.assertTrue(1 <= result["blue"] <= 16)

    def test_generate_batch(self):
        results = DoubleColorBall.generate_batch(3)
        self.assertEqual(len(results), 3)

    def test_validate(self):
        self.assertTrue(DoubleColorBall.validate([1, 2, 3, 4, 5, 6], 7))
        self.assertFalse(DoubleColorBall.validate([1, 1, 2, 3, 4, 5], 7))  # 重复
        self.assertFalse(DoubleColorBall.validate(
            [1, 2, 3, 4, 5, 40], 7))  # 超出范围

    def test_pretty_print(self):
        result = {"red": [1, 2, 3, 4, 5, 6], "blue": 7}
        output = DoubleColorBall.pretty_print(result)
        self.assertIn("01 02 03 04 05 06", output)
        self.assertIn("07", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
