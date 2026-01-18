import unittest
from pkg.calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_addition(self):
        self.assertEqual(self.calculator.evaluate("3 + 5"), 8)
        self.assertEqual(self.calculator.evaluate("10 + -2"), 8)  # Test with negative number

    def test_subtraction(self):
        self.assertEqual(self.calculator.evaluate("10 - 4"), 6)
        self.assertEqual(self.calculator.evaluate("5 - -3"), 8)  # Test with negative number

    def test_multiplication(self):
        self.assertEqual(self.calculator.evaluate("3 * 6"), 18)
        self.assertEqual(self.calculator.evaluate("-2 * 4"), -8)  # Test with negative number

    def test_division(self):
        self.assertEqual(self.calculator.evaluate("10 / 2"), 5)
        self.assertEqual(self.calculator.evaluate("9 / -3"), -3)  # Test with negative number

    def test_mixed_operations(self):
        self.assertEqual(self.calculator.evaluate("3 + 5 * 2"), 13)
        self.assertEqual(self.calculator.evaluate("10 - 4 / 2"), 8)
        self.assertEqual(self.calculator.evaluate("2 + 3 * 4 - 6 / 2"), 11)

    def test_invalid_expression(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("3 +")
        with self.assertRaises(ValueError):
            self.calculator.evaluate("3 5")
        with self.assertRaises(ValueError):
            self.calculator.evaluate("3 + * 5")
        with self.assertRaises(ValueError):
            self.calculator.evaluate("abc")

    def test_empty_expression(self):
        self.assertIsNone(self.calculator.evaluate(""))
        self.assertIsNone(self.calculator.evaluate("   "))
