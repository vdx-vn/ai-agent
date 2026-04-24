import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "skills"


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
        self.assertIn("# Output contract", harness_text)
        self.assertIn("references/overview.md", harness_text)
        self.assertIn("automatic disposable database and filestore cleanup", harness_text)

        overview_text = overview.read_text()
        self.assertIn("## Primary routing rule", overview_text)
        self.assertIn("ODOO_TEST_BASE_CMD", overview_text)
        self.assertIn("dry-run", overview_text)
        self.assertIn("terminate leftover sessions", overview_text)

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

    def test_docs_describe_existing_and_disposable_db_modes(self) -> None:
        expected_snippets = {
            ROOT / "odoo-test" / "SKILL.md": [
                "existing db by default",
                "disposable db by default for install or update validation",
            ],
            ROOT / "odoo-test" / "references" / "overview.md": [
                "current-project-state validation to existing db by default",
                "install and update validation to disposable db by default",
            ],
            ROOT / "odoo-test" / "references" / "checklist.md": [
                "Choose validation DB mode by change surface",
                "Use existing DB mode for unit-style validation on current project state",
                "Use disposable DB mode for install or update validation",
                "Name cleanup expectations explicitly for the chosen DB mode",
            ],
            ROOT / "odoo-test" / "references" / "examples.md": [
                "current project database",
                "disposable database",
            ],
            ROOT / "odoo-local-test-harness" / "SKILL.md": [
                "--db-mode auto|existing|disposable",
                "prefer config `db_name`",
                "multiple candidates",
                "skip DB/filestore cleanup",
                "require explicit DB name",
                "automatic post-run cleanup of DB + filestore",
                "resolved config path",
                "selected DB mode",
            ],
            ROOT / "odoo-local-test-harness" / "references" / "overview.md": [
                "Do not use `dbfilter` to narrow candidates",
                "selected DB or candidate list",
                "cleanup action",
            ],
            ROOT / "odoo-local-test-harness" / "references" / "checklist.md": [
                "prefer config `db_name`",
                "If multiple candidates exist, stop and ask the user which DB to use",
                "Disposable mode requires an explicit DB name",
            ],
            ROOT / "odoo-local-test-harness" / "references" / "examples.md": [
                "existing db by default",
                "disposable db by default",
            ],
        }

        for path, snippets in expected_snippets.items():
            text = path.read_text(encoding="utf-8")
            for snippet in snippets:
                with self.subTest(path=path, snippet=snippet):
                    self.assertIn(snippet, text)


if __name__ == "__main__":
    unittest.main()
