import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class PluginFoundationTests(unittest.TestCase):
    def test_plugin_json_foundation(self) -> None:
        plugin_path = ROOT / ".claude-plugin" / "plugin.json"
        self.assertTrue(plugin_path.exists(), "plugin.json should exist")

        plugin_data = json.loads(plugin_path.read_text(encoding="utf-8"))
        self.assertEqual(plugin_data.get("name"), "odoo-skills")
        self.assertEqual(plugin_data.get("license"), "Apache-2.0")
        self.assertEqual(plugin_data.get("version"), "1.0.0")
        self.assertTrue(plugin_data.get("description"), "description should exist")
        self.assertEqual(plugin_data.get("keywords"), ["odoo", "claude-code", "skills"])

    def test_marketplace_json_foundation(self) -> None:
        marketplace_path = ROOT / ".claude-plugin" / "marketplace.json"
        self.assertTrue(marketplace_path.exists(), "marketplace.json should exist")

        marketplace_data = json.loads(marketplace_path.read_text(encoding="utf-8"))
        self.assertEqual(marketplace_data.get("name"), "odoo-skills-dev")
        self.assertEqual(marketplace_data.get("owner", {}).get("name"), "TruongPX")
        self.assertTrue(marketplace_data.get("metadata", {}).get("description"), "metadata.description should exist")

        plugins = marketplace_data.get("plugins", [])
        self.assertTrue(plugins, "plugins should be non-empty")
        self.assertEqual(plugins[0].get("name"), "odoo-skills")
        self.assertEqual(plugins[0].get("source"), "./")

    def test_readme_mentions_one_command_onboarding_and_manual_fallback(self) -> None:
        readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("git clone git@github.com:vdx-vn/ai-agent", readme_text)
        self.assertIn("cd ai-agent", readme_text)
        self.assertIn("python3 tooling/setup_local.py", readme_text)
        self.assertIn("--docs-root /path/to/odoo/documentation", readme_text)
        self.assertIn("python3 tooling/setup_local.py --uninstall", readme_text)
        self.assertIn("python3 tooling/materialization/materialize_odoo_skill_paths.py", readme_text)
        self.assertIn("claude --plugin-dir ~/.claude/plugins --plugin-dir .", readme_text)

    def test_license_contains_apache_license(self) -> None:
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Apache License", license_text)


if __name__ == "__main__":
    unittest.main()
