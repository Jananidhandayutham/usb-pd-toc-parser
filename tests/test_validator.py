import unittest
from validator import Validator

class TestValidator(unittest.TestCase):
    def test_validation_structure(self):
        toc = [
            {"section_id": "1", "title": "Intro", "page": 1,
             "level": 1, "parent_id": None, "full_path": "1 Intro", "tags": []}
        ]
        spec = [
            {"section_id": "1", "title": "Intro", "page": 1,
             "level": 1, "parent_id": None, "full_path": "1 Intro", "tags": []}
        ]
        validator = Validator(toc, spec)
        parts = validator.compare()
        self.assertIn("comparison", parts)
        self.assertIn("missing_in_spec", parts)
        self.assertEqual(len(parts["comparison"]), 1)
        self.assertTrue(parts["comparison"]["match_overall"].iloc[0])
