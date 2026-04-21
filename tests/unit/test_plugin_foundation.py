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

    def test_readme_prioritizes_global_install_and_links_optional_project_setup_docs(self) -> None:
        readme_text = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertTrue((ROOT / "docs" / "install.md").exists(), "docs/install.md should exist")
        self.assertTrue((ROOT / "docs" / "project-setup.md").exists(), "docs/project-setup.md should exist")

        self.assertIn("git clone git@github.com:vdx-vn/ai-agent", readme_text)
        self.assertIn("python3 -m pip install -e .", readme_text)
        self.assertIn("odoo-skills install-plugin", readme_text)
        self.assertIn("python3 -m tooling.install_plugin", readme_text)
        self.assertIn("## Optional: configure a local Odoo project", readme_text)
        self.assertIn(
            "Only do this if you want local Odoo docs/source paths and local test harness setup inside a specific Odoo repository.",
            readme_text,
        )
        self.assertIn("[docs/install.md](docs/install.md)", readme_text)
        self.assertIn("[docs/project-setup.md](docs/project-setup.md)", readme_text)
        self.assertIn("odoo-skills verify", readme_text)
        self.assertIn("odoo-skills build", readme_text)
        self.assertIn("odoo-skills smoke-install", readme_text)
        self.assertIn("claude --plugin-dir ~/.claude/plugins --plugin-dir .", readme_text)
        self.assertIn("claude plugin marketplace add ./dist/marketplace", readme_text)
        self.assertIn("python3 -m tooling.setup_local", readme_text)
        self.assertIn("deprecated", readme_text.lower())
        self.assertNotIn("## Fastest local marketplace install", readme_text)
        self.assertLess(
            readme_text.index("python3 -m pip install -e ."),
            readme_text.index("odoo-skills install-plugin"),
        )
        self.assertLess(
            readme_text.index("odoo-skills install-plugin"),
            readme_text.index("## Optional: configure a local Odoo project"),
        )

    def test_docs_install_locks_user_local_install_contract(self) -> None:
        install_text = (ROOT / "docs" / "install.md").read_text(encoding="utf-8")

        self.assertIn("for your Claude Code user", install_text)
        self.assertIn("user-local", install_text)
        self.assertIn("does not require an Odoo repository", install_text)
        self.assertIn(
            "does not ask for Odoo docs paths, Odoo source paths, `odoo-bin`, or project config values",
            install_text,
        )
        self.assertIn("## Verify", install_text)
        self.assertIn("claude plugin list --json", install_text)
        self.assertIn("## Troubleshooting", install_text)
        self.assertIn("## Uninstall", install_text)
        self.assertIn("See [project-setup.md](project-setup.md).", install_text)

    def test_docs_project_setup_locks_optional_project_local_setup_contract(self) -> None:
        project_setup_text = (ROOT / "docs" / "project-setup.md").read_text(encoding="utf-8")

        self.assertIn("Use this only after you have already installed `odoo-skills`", project_setup_text)
        self.assertIn("optional and project-local", project_setup_text)
        self.assertIn("From inside the target Odoo repository", project_setup_text)
        self.assertIn("- `.claude/settings.local.json`", project_setup_text)
        self.assertIn("- `.claude/odoo-skill-paths.json`", project_setup_text)
        self.assertIn("`ODOO_TEST_BASE_CMD`", project_setup_text)
        self.assertIn(
            "These files are separate from the user-local Claude Code plugin installation.",
            project_setup_text,
        )

    def test_license_contains_apache_license(self) -> None:
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Apache License", license_text)


if __name__ == "__main__":
    unittest.main()
