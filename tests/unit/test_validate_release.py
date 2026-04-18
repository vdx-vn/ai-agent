import unittest

from tooling.validation.release import scan_release_text


class ValidateReleaseTests(unittest.TestCase):
    def test_unresolved_odoo_placeholder_is_reported(self) -> None:
        self.assertEqual(
            scan_release_text("Use <ODOO_DOCS_ROOT> here"),
            ["unresolved Odoo placeholder"],
        )


if __name__ == "__main__":
    unittest.main()
