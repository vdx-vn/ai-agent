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

    def test_odoo_test_agent_prompt_uses_precise_harness_boundary(self) -> None:
        prompt = (ROOT / "odoo-test" / "agents" / "openai.yaml").read_text()
        self.assertIn(
            "Compose with $odoo-local-test-harness when local execution depends on ODOO_TEST_BASE_CMD, config inspection, existing-db resolution, or disposable DB/filestore cleanup.",
            prompt,
        )
        self.assertNotIn("shared cleanup", prompt)

    def test_docs_do_not_allow_existing_mode_override_for_install_or_update(self) -> None:
        paths = [
            ROOT / "odoo-test" / "references" / "checklist.md",
            ROOT / "odoo-local-test-harness" / "SKILL.md",
            ROOT / "odoo-local-test-harness" / "references" / "overview.md",
            ROOT / "odoo-local-test-harness" / "references" / "checklist.md",
        ]

        for path in paths:
            with self.subTest(path=path):
                self.assertNotIn(
                    "unless the user explicitly overrides",
                    path.read_text(encoding="utf-8"),
                )

    def test_docs_describe_existing_and_disposable_db_modes(self) -> None:
        expected_snippets = {
            ROOT / "odoo-test" / "SKILL.md": [
                "current-state validation uses an existing db by default",
                "install, update, or explicit disposable validation uses a disposable db",
                "never clean DB/filestore in existing mode",
                "always clean DB + filestore after disposable runs",
            ],
            ROOT / "odoo-test" / "references" / "overview.md": [
                "current-project-state validation to existing db by default",
                "install, update, or explicit disposable validation to disposable db by default",
                "Existing-db validation must not clean DB or filestore",
                "Disposable-db validation must clean DB and filestore after execution",
            ],
            ROOT / "odoo-test" / "references" / "checklist.md": [
                "Choose validation DB mode by change surface",
                "Use existing DB mode for current-project-state validation",
                "Use disposable DB mode for install, update, or explicit disposable validation",
                "Name cleanup expectations explicitly for the chosen DB mode",
                "Confirm existing mode skips DB/filestore cleanup",
                "Confirm disposable mode cleans DB + filestore after execution",
            ],
            ROOT / "odoo-test" / "references" / "examples.md": [
                "current project database",
                "disposable database",
            ],
            ROOT / "odoo-local-test-harness" / "SKILL.md": [
                "--db-mode auto|existing|disposable",
                "prefer config `db_name`",
                "multiple candidates",
                "existing mode must never clean DB/filestore",
                "install, update, or explicit disposable mode requires explicit `--db`",
                "automatic post-run cleanup of DB + filestore",
                "resolved config path",
                "selected DB mode",
            ],
            ROOT / "odoo-local-test-harness" / "references" / "overview.md": [
                "Do not use `dbfilter` to narrow candidates",
                "selected DB or candidate list",
                "cleanup action",
                "Existing mode must not clean DB or filestore",
                "Disposable mode must clean DB and filestore after execution",
            ],
            ROOT / "odoo-local-test-harness" / "references" / "checklist.md": [
                "prefer config `db_name`",
                "If multiple candidates exist, stop and ask the user which DB to use",
                "Disposable mode requires an explicit DB name",
                "Existing mode must not clean DB/filestore",
                "Disposable mode must clean DB + filestore after execution",
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
