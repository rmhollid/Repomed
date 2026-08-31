import unittest
from repomedic.engine import RepairEngine

class EngineTests(unittest.TestCase):
    def test_candidate_generation_contains_division(self):
        src = "def divide(a, b):\n    return a * b\n"
        candidates = RepairEngine._candidate_patches(src)
        replacements = {c["replacement"] for c in candidates}
        self.assertIn("return a / b", replacements)

if __name__ == "__main__":
    unittest.main()
