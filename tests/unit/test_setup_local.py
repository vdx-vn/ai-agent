import subprocess
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch

from tooling.setup_local import main, parse_args, run_setup, run_uninstall


ROOT = Path(__file__).resolve().parents[2]


class ParseArgsTests(unittest.TestCase):
    def test_parse_args_keeps_legacy_options_for_compatibility(self) -> None:
        args = parse_args(
            [
                "--docs-root",
                "/tmp/docs",
                "--source-root",
                "/tmp/src",
                "--version",
                "18.0",
                "--python-bin",
                "python3.11",
                "--odoo-bin",
                "/tmp/odoo-bin",
                "--config",
                "/tmp/odoo.conf",
                "--base-cmd",
                'python3 "/tmp/odoo-bin" -c "/tmp/odoo.conf"',
                "--yes",
                "--uninstall",
            ]
        )

        self.assertEqual(args.docs_root, "/tmp/docs")
        self.assertEqual(args.source_root, "/tmp/src")
        self.assertEqual(args.version, "18.0")
        self.assertEqual(args.python_bin, "python3.11")
        self.assertEqual(args.odoo_bin, "/tmp/odoo-bin")
        self.assertEqual(args.config, "/tmp/odoo.conf")
        self.assertEqual(args.base_cmd, 'python3 "/tmp/odoo-bin" -c "/tmp/odoo.conf"')
        self.assertTrue(args.yes)
        self.assertTrue(args.uninstall)


class SetupShimTests(unittest.TestCase):
    def test_run_setup_prints_deprecation_and_delegates_to_install_plugin(self) -> None:
        repo_root = ROOT
        args = Namespace(
            docs_root="/tmp/docs",
            source_root="/tmp/src",
            version="18.0",
            python_bin="python3",
            odoo_bin="/tmp/odoo-bin",
            config="/tmp/odoo.conf",
            base_cmd='python3 "/tmp/odoo-bin" -c "/tmp/odoo.conf"',
            yes=True,
            uninstall=False,
        )

        with patch("tooling.setup_local.run_install_plugin", return_value=0) as run_install_mock:
            with patch("builtins.print") as print_mock:
                result = run_setup(repo_root, args)

        self.assertEqual(result, 0)
        run_install_mock.assert_called_once_with(repo_root, args)
        printed = "\n".join(call.args[0] for call in print_mock.call_args_list)
        printed_lower = printed.lower()
        self.assertIn("deprecated", printed_lower)
        self.assertIn("legacy compatibility command", printed_lower)
        self.assertIn("odoo-skills install-plugin", printed)
        self.assertIn("python3 -m tooling.install_plugin", printed)
        self.assertIn("only when configuring a local odoo repository", printed_lower)

    def test_run_uninstall_prints_deprecation_and_delegates_to_install_plugin(self) -> None:
        repo_root = ROOT
        args = Namespace(uninstall=True)

        with patch("tooling.setup_local.run_uninstall_plugin", return_value=0) as run_uninstall_mock:
            with patch("builtins.print") as print_mock:
                result = run_uninstall(repo_root, args)

        self.assertEqual(result, 0)
        run_uninstall_mock.assert_called_once_with(repo_root, args)
        printed = "\n".join(call.args[0] for call in print_mock.call_args_list)
        printed_lower = printed.lower()
        self.assertIn("deprecated", printed_lower)
        self.assertIn("legacy compatibility command", printed_lower)
        self.assertIn("odoo-skills install-plugin", printed)
        self.assertIn("python3 -m tooling.install_plugin", printed)
        self.assertIn("only when configuring a local odoo repository", printed_lower)


class DirectExecutionTests(unittest.TestCase):
    def test_setup_local_script_runs_when_invoked_by_file_path(self) -> None:
        result = subprocess.run(
            ["python3", str(ROOT / "tooling" / "setup_local.py"), "--help"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertIn("deprecated", result.stdout.lower())


class MainTests(unittest.TestCase):
    def test_main_dispatches_to_setup_when_not_uninstalling(self) -> None:
        args = Namespace(uninstall=False)
        expected_repo_root = Path(__file__).resolve().parents[2]

        with patch("tooling.setup_local.parse_args", return_value=args):
            with patch("tooling.setup_local.run_setup", return_value=0) as run_setup_mock:
                result = main([])

        self.assertEqual(result, 0)
        run_setup_mock.assert_called_once_with(expected_repo_root, args)

    def test_main_dispatches_to_uninstall_when_requested(self) -> None:
        args = Namespace(uninstall=True)
        expected_repo_root = Path(__file__).resolve().parents[2]

        with patch("tooling.setup_local.parse_args", return_value=args):
            with patch("tooling.setup_local.run_uninstall", return_value=0) as run_uninstall_mock:
                result = main([])

        self.assertEqual(result, 0)
        run_uninstall_mock.assert_called_once_with(expected_repo_root, args)


if __name__ == "__main__":
    unittest.main()
