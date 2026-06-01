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

            plugin_root = output_dir / "plugins" / "odoo-skills-v19"
            self.assertTrue((output_dir / ".agents" / "plugins" / "marketplace.json").exists())
            self.assertTrue((output_dir / ".claude-plugin" / "marketplace.json").exists())
            self.assertTrue((plugin_root / ".codex-plugin" / "plugin.json").exists())
            self.assertTrue((plugin_root / ".claude-plugin" / "plugin.json").exists())
            self.assertTrue((output_dir / ".claude-plugin" / "marketplace.json").exists())
            self.assertTrue((plugin_root / "skills" / "odoo-build" / "SKILL.md").exists())
            self.assertTrue((output_dir / "README.md").exists())
            self.assertTrue((output_dir / "LICENSE").exists())

            codex_marketplace = (output_dir / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8")
            self.assertIn('"path": "./plugins/odoo-skills-v19"', codex_marketplace)

            runtime_readme = (output_dir / "README.md").read_text(encoding="utf-8")
            self.assertIn("Runtime marketplace bundle", runtime_readme)
            self.assertIn("## Codex CLI", runtime_readme)
            self.assertIn("codex plugin marketplace add ./dist/marketplace", runtime_readme)
            self.assertIn("## Claude Code", runtime_readme)
            self.assertIn("claude plugin marketplace add ./dist/marketplace", runtime_readme)
            self.assertIn("claude plugin install odoo-skills@odoo-skills-dev --scope local", runtime_readme)
            self.assertIn("## Optional: configure a local Odoo project", runtime_readme)
            self.assertIn("python3 -m pip install -e .", runtime_readme)
            self.assertIn("odoo-skills project-setup", runtime_readme)
            self.assertIn("# fallback", runtime_readme)
            self.assertIn("python3 -m tooling.cli project-setup", runtime_readme)
            self.assertIn("Optional for local Odoo repositories only", runtime_readme)
            self.assertIn(
                "These follow-up commands must be run from a clone of the source repository, not from this runtime bundle.",
                runtime_readme,
            )
            self.assertIn("Install the repository CLI entrypoints from that separate source-repo clone first", runtime_readme)
            self.assertNotIn("odoo-skills-build", runtime_readme)
            self.assertNotIn("## Fastest local marketplace install", runtime_readme)
            self.assertLess(
                runtime_readme.index("claude plugin marketplace add ./dist/marketplace"),
                runtime_readme.index("claude plugin install odoo-skills@odoo-skills-dev --scope local"),
            )
            self.assertLess(
                runtime_readme.index("python3 -m pip install -e ."),
                runtime_readme.index("odoo-skills project-setup"),
            )
            self.assertNotIn("python3 tooling/setup_local.py", runtime_readme)
            self.assertNotIn("tooling/materialization/materialize_odoo_skill_paths.py", runtime_readme)
            self.assertNotIn(".claude/skills/odoo-paths.md", runtime_readme)

            self.assertFalse((output_dir / "skill-creator").exists())
            self.assertFalse((output_dir / ".claude" / "skills").exists())
            self.assertFalse((output_dir / "odoo-test").exists())

            top_level_entries = {path.name for path in output_dir.iterdir()}
            self.assertEqual(top_level_entries, {".agents", ".claude-plugin", "plugins", "README.md", "LICENSE"})


if __name__ == "__main__":
    unittest.main()
