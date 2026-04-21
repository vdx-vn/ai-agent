import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tooling.materialization.materialize_odoo_skill_paths import parse_args


ROOT = Path(__file__).resolve().parents[2]
COPIED_SUGGEST_PATH = ROOT / ".claude" / "skills" / "scripts" / "suggest_odoo_skill_setup.py"
_spec = importlib.util.spec_from_file_location("copied_suggest_odoo_skill_setup", COPIED_SUGGEST_PATH)
assert _spec and _spec.loader
_copied_suggest = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_copied_suggest)
build_system_message = _copied_suggest.build_system_message

PROJECT_SETUP_COMMAND = "odoo-skills project-setup"
PROJECT_SETUP_FALLBACK = "python3 -m tooling.cli project-setup"


class SuggestOdooSkillSetupTests(unittest.TestCase):
    def test_missing_base_command_adds_odoo_test_base_cmd_message(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            (repo_root / "odoo-bin").write_text("", encoding="utf-8")

            message = build_system_message(
                raw="",
                repo_root=repo_root,
                mode="session-start",
            )

            self.assertIn("ODOO_TEST_BASE_CMD", message)

    def test_dev_settings_use_tooling_materialization_script_path(self) -> None:
        settings = (ROOT / ".claude" / "settings.json").read_text(encoding="utf-8")
        self.assertIn(
            'tooling/materialization/suggest_odoo_skill_setup.py',
            settings,
        )

    def test_setup_guidance_points_to_project_setup_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)

            message = build_system_message(
                raw="create new odoo module",
                repo_root=repo_root,
                mode="prompt-submit",
            )

            self.assertIn("python3 -m pip install -e .", message)
            self.assertIn(PROJECT_SETUP_COMMAND, message)
            self.assertIn(PROJECT_SETUP_FALLBACK, message)
            self.assertNotIn("python3 tooling/setup_local.py", message)
            self.assertNotIn(
                "python3 tooling/materialization/materialize_odoo_skill_paths.py",
                message,
            )
            self.assertIn(".claude/settings.local.json", message)
            self.assertIn("ODOO_TEST_BASE_CMD", message)

    def test_copied_path_docs_match_expected_guidance(self) -> None:
        for doc_path in [
            ROOT / ".claude" / "skills" / "odoo-paths.md",
            ROOT / "docs" / "reference" / "odoo-paths.md",
            ROOT / "docs" / "authoring" / "odoo-paths.md",
        ]:
            with self.subTest(doc=str(doc_path)):
                content = doc_path.read_text(encoding="utf-8")
                self.assertIn("python3 -m pip install -e .", content)
                self.assertIn(PROJECT_SETUP_COMMAND, content)
                self.assertIn(PROJECT_SETUP_FALLBACK, content)
                self.assertNotIn("python3 tooling/setup_local.py", content)
                self.assertNotIn(
                    "python3 tooling/materialization/materialize_odoo_skill_paths.py",
                    content,
                )
                self.assertNotIn("/home/xmars/dev/odoo/doc-18", content)
                self.assertNotIn("/home/xmars/dev/odoo/ce-18", content)
                self.assertIn("<ODOO_DOCS_ROOT>", content)
                self.assertIn("<ODOO_SOURCE_ROOT>", content)
                self.assertIn(".claude/settings.local.json", content)
                self.assertIn("ODOO_TEST_BASE_CMD", content)

    def test_materialize_parse_args_defaults_use_repo_claude_paths(self) -> None:
        with patch(
            "sys.argv",
            [
                "materialize_odoo_skill_paths.py",
                "--docs-root",
                "/tmp/docs",
                "--source-root",
                "/tmp/src",
            ],
        ):
            args = parse_args()

        expected_project_root = ROOT
        self.assertEqual(args.skills_root, str(expected_project_root / ".claude" / "skills"))
        self.assertEqual(args.config_path, str(expected_project_root / ".claude" / "odoo-skill-paths.json"))


if __name__ == "__main__":
    unittest.main()
