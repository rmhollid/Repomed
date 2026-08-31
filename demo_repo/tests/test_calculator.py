import unittest
from calculator import divide

class CalculatorTests(unittest.TestCase):
    def test_divide(self):
        self.assertEqual(divide(8, 2), 4)
        self.assertEqual(divide(9, 3), 3)

if __name__ == "__main__":
    unittest.main()
