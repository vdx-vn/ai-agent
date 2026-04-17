import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import suggest_odoo_skill_setup as suggest  # type: ignore


class SuggestOdooSkillSetupTests(unittest.TestCase):
    def make_repo(self) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        repo_root = Path(temp_dir.name)
        (repo_root / "addons").mkdir()
        (repo_root / ".claude").mkdir()
        return repo_root

    def test_missing_base_command_adds_harness_message(self) -> None:
        repo_root = self.make_repo()
        message = suggest.build_system_message("", repo_root, "session-start")
        self.assertIn("ODOO_TEST_BASE_CMD", message)
        self.assertIn(".claude/settings.local.json", message)

    def test_existing_base_command_suppresses_harness_message(self) -> None:
        repo_root = self.make_repo()
        (repo_root / ".claude" / "settings.local.json").write_text(
            json.dumps(
                {
                    "env": {
                        "ODOO_TEST_BASE_CMD": "python3 /opt/odoo/odoo-bin -c /tmp/odoo.conf"
                    }
                }
            )
        )
        message = suggest.build_system_message("", repo_root, "session-start")
        self.assertNotIn("ODOO_TEST_BASE_CMD", message)

    def test_unrelated_prompt_submit_does_not_add_harness_message(self) -> None:
        repo_root = self.make_repo()
        message = suggest.build_system_message("hello unrelated", repo_root, "prompt-submit")
        self.assertNotIn("ODOO_TEST_BASE_CMD", message)

    def test_malformed_settings_local_json_adds_parse_error_message(self) -> None:
        repo_root = self.make_repo()
        (repo_root / ".claude" / "settings.local.json").write_text('{"env":')
        message = suggest.build_system_message("", repo_root, "session-start")
        self.assertIn("malformed `.claude/settings.local.json`", message)
        self.assertNotIn("Detected Odoo project without local test command", message)


if __name__ == "__main__":
    unittest.main()
