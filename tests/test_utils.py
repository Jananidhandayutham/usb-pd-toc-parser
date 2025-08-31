import unittest
from utils import normalize_title, parent_of, level_of

class TestUtils(unittest.TestCase):
    def test_normalize_title(self):
        self.assertEqual(normalize_title("Section 1.... Title"), "Section 1 Title")

    def test_parent_of(self):
        self.assertEqual(parent_of("2.1.3"), "2.1")
        self.assertEqual(parent_of("1"), None)

    def test_level_of(self):
        self.assertEqual(level_of("2.1.3"), 3)
        self.assertEqual(level_of("1"), 1)
