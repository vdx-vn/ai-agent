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
        self.assertIn("Codex CLI can read that file directly", harness_text)
        self.assertIn("shell_environment_policy", harness_text)
        self.assertIn("Do not use `ODOO_TEST` or `DB`", harness_text)

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
            "Compose with $odoo-local-test-harness when local execution depends on ODOO_TEST_BASE_CMD or shared DB and filestore cleanup.",
            prompt,
        )

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

    def test_docs_describe_legacy_disposable_cleanup_harness(self) -> None:
        expected_snippets = {
            ROOT / "odoo-test" / "SKILL.md": [
                "use a named disposable database when local harness execution is requested",
                "compose with shared DB and filestore cleanup when local execution uses the harness",
            ],
            ROOT / "odoo-test" / "references" / "overview.md": [
                "Use a named disposable database when local harness execution is requested",
                "Compose with shared DB and filestore cleanup when local execution uses `odoo-local-test-harness`",
            ],
            ROOT / "odoo-test" / "references" / "checklist.md": [
                "Identify whether local execution needs `odoo-local-test-harness`",
                "Use a named disposable database when local harness execution is requested",
                "Confirm shared cleanup expectations when the local harness is used",
            ],
            ROOT / "odoo-test" / "references" / "examples.md": [
                "project-local Odoo command",
                "shared DB and filestore cleanup",
            ],
            ROOT / "odoo-local-test-harness" / "SKILL.md": [
                "requested disposable database name",
                "Normalize `-d`, `--test-tags`, `--test-enable`, `-i`, `-u`, and `--stop-after-init`",
                "automatic post-run cleanup through `scripts/delete_unused_odoo_db.py`",
                "cleanup action performed or skipped",
            ],
            ROOT / "odoo-local-test-harness" / "references" / "overview.md": [
                "shared local cleanup behavior",
                "Preserve the configured config path from the base command",
                "Use shared automatic post-run cleanup only for disposable local database flows",
            ],
            ROOT / "odoo-local-test-harness" / "references" / "checklist.md": [
                "Keep automatic post-run cleanup for disposable databases and matching filestore state",
                "Return whether pre-run cleanup ran",
                "Return that post-run cleanup is automatic for real runs",
            ],
            ROOT / "odoo-local-test-harness" / "references" / "examples.md": [
                "require a target disposable db if execution is requested",
                "shared cleanup",
            ],
        }

        for path, snippets in expected_snippets.items():
            text = path.read_text(encoding="utf-8")
            for snippet in snippets:
                with self.subTest(path=path, snippet=snippet):
                    self.assertIn(snippet, text)


if __name__ == "__main__":
    unittest.main()
