import unittest
from pathlib import Path

from tooling.validate_plugin import validate_plugin


ROOT = Path(__file__).resolve().parents[2]


class ValidateFrontmatterTests(unittest.TestCase):
    def test_validate_plugin_is_clean_for_repo(self) -> None:
        self.assertEqual(validate_plugin(ROOT), [])


if __name__ == "__main__":
    unittest.main()
