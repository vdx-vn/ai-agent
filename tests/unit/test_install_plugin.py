import subprocess
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch

from tooling.install_plugin import main, parse_args, run_install


ROOT = Path(__file__).resolve().parents[2]


class InstallPluginContractTests(unittest.TestCase):
    def test_install_plugin_module_exists(self) -> None:
        self.assertTrue((ROOT / "tooling" / "install_plugin.py").exists())

    def test_pyproject_exposes_install_plugin_console_script(self) -> None:
        pyproject_text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('odoo-skills-install = "tooling.install_plugin:main"', pyproject_text)

    def test_parse_args_supports_uninstall(self) -> None:
        args = parse_args(["--uninstall"])
        self.assertTrue(args.uninstall)

    def test_install_plugin_script_help_runs_by_file_path(self) -> None:
        result = subprocess.run(
            ["python3", str(ROOT / "tooling" / "install_plugin.py"), "--help"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertIn("install local odoo-skills plugin bundle", result.stdout.lower())

    def test_main_dispatches_to_install_when_not_uninstalling(self) -> None:
        args = Namespace(uninstall=False)
        expected_repo_root = ROOT

        with patch("tooling.install_plugin.parse_args", return_value=args):
            with patch("tooling.install_plugin.run_install", return_value=0) as run_install_mock:
                result = main([])

        self.assertEqual(result, 0)
        run_install_mock.assert_called_once_with(expected_repo_root, args)

    def test_main_dispatches_to_uninstall_when_requested(self) -> None:
        args = Namespace(uninstall=True)
        expected_repo_root = ROOT

        with patch("tooling.install_plugin.parse_args", return_value=args):
            with patch("tooling.install_plugin.run_uninstall", return_value=0) as run_uninstall_mock:
                result = main([])

        self.assertEqual(result, 0)
        run_uninstall_mock.assert_called_once_with(expected_repo_root, args)


class RunInstallMessageTests(unittest.TestCase):
    def test_run_install_prints_optional_project_setup_guidance(self) -> None:
        with patch("tooling.install_plugin.ensure_claude_cli"):
            with patch("tooling.install_plugin.build_marketplace", return_value=ROOT / "dist" / "marketplace"):
                with patch("tooling.install_plugin.run_command"):
                    with patch("builtins.print") as print_mock:
                        result = run_install(ROOT, Namespace(uninstall=False))

        self.assertEqual(result, 0)
        printed = "\n".join(call.args[0] for call in print_mock.call_args_list)
        self.assertIn("Plugin install complete", printed)
        self.assertIn("python3 -m pip install -e .", printed)
        self.assertIn("Optional for local Odoo repositories only", printed)
        self.assertIn("odoo-skills project-setup", printed)
        self.assertIn("python3 -m tooling.cli project-setup", printed)


if __name__ == "__main__":
    unittest.main()
