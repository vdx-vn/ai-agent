import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tooling.materialization.materialize_odoo_skill_paths import parse_args
from tooling.materialization.suggest_odoo_skill_setup import build_system_message


ROOT = Path(__file__).resolve().parents[2]


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

    def test_setup_guidance_points_to_tooling_materialization_script(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)

            message = build_system_message(
                raw="create new odoo module",
                repo_root=repo_root,
                mode="prompt-submit",
            )

            self.assertIn(
                "python3 tooling/materialization/materialize_odoo_skill_paths.py",
                message,
            )

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
