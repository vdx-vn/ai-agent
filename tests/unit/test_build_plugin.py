import shutil
import tempfile
import unittest
from pathlib import Path

from tooling.build_plugin import build_marketplace


ROOT = Path(__file__).resolve().parents[2]


class BuildPluginTests(unittest.TestCase):
    def test_build_marketplace_creates_runtime_subset_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "marketplace"
            output_dir.mkdir(parents=True)
            (output_dir / "stale.txt").write_text("stale", encoding="utf-8")

            built_path = build_marketplace(ROOT, output_dir)

            self.assertEqual(built_path, output_dir)
            self.assertFalse((output_dir / "stale.txt").exists())

            self.assertTrue((output_dir / ".claude-plugin" / "plugin.json").exists())
            self.assertTrue((output_dir / ".claude-plugin" / "marketplace.json").exists())
            self.assertTrue((output_dir / "skills" / "odoo-build" / "SKILL.md").exists())
            self.assertTrue((output_dir / "README.md").exists())
            self.assertTrue((output_dir / "LICENSE").exists())

            runtime_readme = (output_dir / "README.md").read_text(encoding="utf-8")
            self.assertIn("Runtime marketplace bundle", runtime_readme)
            self.assertIn("claude plugin install odoo-skills@odoo-skills-dev --scope local", runtime_readme)
            self.assertIn("claude plugin marketplace add ./dist/marketplace", runtime_readme)
            self.assertIn("claude plugin list --json", runtime_readme)
            self.assertLess(
                runtime_readme.index("claude plugin marketplace add ./dist/marketplace"),
                runtime_readme.index("## Install and use plugin"),
            )
            self.assertIn("odoo-skills project-setup", runtime_readme)
            self.assertIn("python3 -m tooling.cli project-setup", runtime_readme)
            self.assertNotIn("python3 tooling/setup_local.py", runtime_readme)
            self.assertNotIn("tooling/materialization/materialize_odoo_skill_paths.py", runtime_readme)
            self.assertNotIn(".claude/skills/odoo-paths.md", runtime_readme)

            self.assertFalse((output_dir / "skill-creator").exists())
            self.assertFalse((output_dir / ".claude" / "skills").exists())
            self.assertFalse((output_dir / "odoo-test").exists())

            top_level_entries = {path.name for path in output_dir.iterdir()}
            self.assertEqual(top_level_entries, {".claude-plugin", "skills", "README.md", "LICENSE"})


if __name__ == "__main__":
    unittest.main()
