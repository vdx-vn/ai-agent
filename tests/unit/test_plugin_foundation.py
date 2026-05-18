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

    def test_codex_plugin_json_foundation(self) -> None:
        plugin_path = ROOT / ".codex-plugin" / "plugin.json"
        self.assertTrue(plugin_path.exists(), "Codex plugin.json should exist")

        plugin_data = json.loads(plugin_path.read_text(encoding="utf-8"))
        self.assertEqual(plugin_data.get("name"), "odoo-skills")
        self.assertEqual(plugin_data.get("license"), "Apache-2.0")
        self.assertEqual(plugin_data.get("version"), "1.0.0")
        self.assertEqual(plugin_data.get("skills"), "./skills/")
        self.assertTrue(plugin_data.get("interface", {}).get("displayName"))
        self.assertIn("codex", plugin_data.get("keywords", []))

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
        self.assertEqual(plugins[0].get("source"), "./dist/marketplace/plugins/odoo-skills")

    def test_codex_marketplace_json_foundation(self) -> None:
        marketplace_path = ROOT / ".agents" / "plugins" / "marketplace.json"
        self.assertTrue(marketplace_path.exists(), "Codex marketplace.json should exist")

        marketplace_data = json.loads(marketplace_path.read_text(encoding="utf-8"))
        self.assertEqual(marketplace_data.get("name"), "odoo-skills-dev")
        self.assertEqual(marketplace_data.get("interface", {}).get("displayName"), "Odoo Skills Dev")

        plugins = marketplace_data.get("plugins", [])
        self.assertTrue(plugins, "plugins should be non-empty")
        self.assertEqual(plugins[0].get("name"), "odoo-skills")
        self.assertEqual(plugins[0].get("source", {}).get("path"), "./dist/marketplace/plugins/odoo-skills")
        self.assertEqual(plugins[0].get("policy", {}).get("installation"), "AVAILABLE")
        self.assertEqual(plugins[0].get("policy", {}).get("authentication"), "ON_INSTALL")
        self.assertEqual(plugins[0].get("category"), "Coding")

    def test_readme_has_one_installation_section_with_codex_and_claude_parts(self) -> None:
        readme_text = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertTrue((ROOT / "docs" / "install.md").exists(), "docs/install.md should exist")
        self.assertTrue((ROOT / "docs" / "project-setup.md").exists(), "docs/project-setup.md should exist")

        self.assertEqual(readme_text.count("## Installation"), 1)
        self.assertIn("git clone git@github.com:vdx-vn/ai-agent", readme_text)
        self.assertIn("python3 -m pip install -e .", readme_text)
        self.assertIn("### Codex CLI", readme_text)
        self.assertIn("npm install -g @openai/codex", readme_text)
        self.assertIn("brew install --cask codex", readme_text)
        self.assertIn('export ODOO_SKILLS_REPO="$PWD"', readme_text)
        self.assertIn("codex login", readme_text)
        self.assertIn("odoo-skills build", readme_text)
        self.assertIn('codex plugin marketplace add "$ODOO_SKILLS_REPO/dist/marketplace"', readme_text)
        self.assertIn("codex plugin marketplace add /absolute/path/to/ai-agent/dist/marketplace", readme_text)
        self.assertIn("not the Odoo/project repository where you want to use the skills", readme_text)
        self.assertIn("codex plugin marketplace remove odoo-skills-dev", readme_text)
        self.assertIn("Inside Codex, open `/plugins`, search for `odoo-skills`, and install the local plugin.", readme_text)
        self.assertIn("OpenAI Codex CLI getting started", readme_text)
        self.assertIn("### Claude Code", readme_text)
        self.assertIn("odoo-skills install-plugin", readme_text)
        self.assertIn("python3 -m tooling.install_plugin", readme_text)
        self.assertIn("## Optional Project Setup", readme_text)
        self.assertIn(
            "Only do this if you want local Odoo docs/source paths and local test harness setup inside a specific Odoo repository.",
            readme_text,
        )
        self.assertIn("[docs/install.md](docs/install.md)", readme_text)
        self.assertIn("[docs/project-setup.md](docs/project-setup.md)", readme_text)
        self.assertIn("odoo-skills verify", readme_text)
        self.assertIn("odoo-skills build", readme_text)
        self.assertIn("odoo-skills smoke-install", readme_text)
        self.assertIn("python3 -m tooling.setup_local", readme_text)
        self.assertIn("deprecated", readme_text.lower())
        self.assertNotIn("## Fastest local marketplace install", readme_text)
        self.assertLess(
            readme_text.index("python3 -m pip install -e ."),
            readme_text.index("### Codex CLI"),
        )
        self.assertLess(
            readme_text.index("### Codex CLI"),
            readme_text.index("### Claude Code"),
        )
        self.assertLess(
            readme_text.index("### Claude Code"),
            readme_text.index("## Optional Project Setup"),
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

        self.assertIn("Use this after you have installed `odoo-skills` for Codex CLI or Claude Code.", project_setup_text)
        self.assertIn("optional and project-local", project_setup_text)
        self.assertIn("From inside the target Odoo repository", project_setup_text)
        self.assertIn("- `.odoo-skills/project.json`", project_setup_text)
        self.assertIn("- `.claude/settings.local.json`", project_setup_text)
        self.assertIn("- `.claude/odoo-skill-paths.json`", project_setup_text)
        self.assertIn("`ODOO_TEST_BASE_CMD`", project_setup_text)
        self.assertIn("`odooTestBaseCmd`", project_setup_text)
        self.assertIn(
            "These files are separate from the user-local agent plugin installation.",
            project_setup_text,
        )

    def test_license_contains_apache_license(self) -> None:
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Apache License", license_text)


if __name__ == "__main__":
    unittest.main()
