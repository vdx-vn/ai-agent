import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class OdooLocalTestHarnessDocsTests(unittest.TestCase):
    def test_harness_skill_exists_with_required_contract(self) -> None:
        harness = ROOT / "odoo-local-test-harness" / "SKILL.md"
        overview = ROOT / "odoo-local-test-harness" / "references" / "overview.md"
        self.assertTrue(harness.exists(), harness)
        self.assertTrue(overview.exists(), overview)
        harness_text = harness.read_text()
        self.assertIn("ODOO_TEST_BASE_CMD", harness_text)
        self.assertIn("odoo-test", harness_text)
        self.assertIn("odoo-delivery-ops", harness_text)
        self.assertIn("## Output contract", harness_text)
        self.assertIn("references/overview.md", harness_text)

        overview_text = overview.read_text()
        self.assertIn("## Primary routing rule", overview_text)
        self.assertIn("ODOO_TEST_BASE_CMD", overview_text)
        self.assertIn("dry-run", overview_text)

    def test_sibling_skills_reference_harness(self) -> None:
        odoo_test = (ROOT / "odoo-test" / "SKILL.md").read_text()
        delivery_ops = (ROOT / "odoo-delivery-ops" / "SKILL.md").read_text()
        self.assertIn("odoo-local-test-harness", odoo_test)
        self.assertIn("odoo-local-test-harness", delivery_ops)
        self.assertIn("- `odoo-local-test-harness`", delivery_ops)

    def test_task5_reference_and_agent_artifacts_reference_harness(self) -> None:
        expected_mentions = {
            ROOT / "odoo-test" / "references" / "overview.md": "odoo-local-test-harness",
            ROOT / "odoo-test" / "references" / "checklist.md": "odoo-local-test-harness",
            ROOT / "odoo-test" / "references" / "examples.md": "odoo-local-test-harness",
            ROOT / "odoo-test" / "agents" / "openai.yaml": "$odoo-local-test-harness",
            ROOT / "odoo-delivery-ops" / "references" / "overview.md": "odoo-local-test-harness",
            ROOT / "odoo-delivery-ops" / "references" / "checklist.md": "odoo-local-test-harness",
            ROOT / "odoo-delivery-ops" / "references" / "examples.md": "odoo-local-test-harness",
            ROOT / "odoo-delivery-ops" / "agents" / "openai.yaml": "$odoo-local-test-harness",
        }

        for path, expected in expected_mentions.items():
            with self.subTest(path=path):
                self.assertIn(expected, path.read_text())


if __name__ == "__main__":
    unittest.main()
