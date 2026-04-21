import json
import subprocess
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch

from tooling.cli import main as cli_main
from tooling.local_setup_common import repo_looks_odoo, resolve_project_root
from tooling.project_setup import parse_args, run_project_setup


class ProjectRootHelpersTests(unittest.TestCase):
    def test_repo_looks_odoo_accepts_manifest_near_repo_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            addon_dir = repo_root / "sale_ext"
            addon_dir.mkdir()
            (addon_dir / "__manifest__.py").write_text("{}\n", encoding="utf-8")

            self.assertTrue(repo_looks_odoo(repo_root))

    def test_resolve_project_root_prefers_git_toplevel(self) -> None:
        start = Path("/tmp/work/custom/addons/demo")
        result = subprocess.CompletedProcess(
            ["git"],
            0,
            stdout="/tmp/work/custom\n",
            stderr="",
        )

        with patch("tooling.local_setup_common.subprocess.run", return_value=result):
            resolved = resolve_project_root(start)

        self.assertEqual(resolved, Path("/tmp/work/custom"))

    def test_resolve_project_root_falls_back_to_current_directory_when_git_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            start = Path(tmp)

            with patch("tooling.local_setup_common.subprocess.run", side_effect=OSError("git missing")):
                resolved = resolve_project_root(start)

        self.assertEqual(resolved, start.resolve())



class ProjectSetupParseArgsTests(unittest.TestCase):
    def test_parse_args_supports_project_setup_options(self) -> None:
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
                "--yes",
                "--force",
                "--dry-run",
            ]
        )

        self.assertEqual(args.docs_root, "/tmp/docs")
        self.assertEqual(args.source_root, "/tmp/src")
        self.assertEqual(args.version, "18.0")
        self.assertEqual(args.python_bin, "python3.11")
        self.assertEqual(args.odoo_bin, "/tmp/odoo-bin")
        self.assertEqual(args.config, "/tmp/odoo.conf")
        self.assertTrue(args.yes)
        self.assertTrue(args.force)
        self.assertTrue(args.dry_run)

    def test_parse_args_rejects_base_cmd_with_odoo_bin_or_config(self) -> None:
        with self.assertRaises(SystemExit):
            parse_args(["--base-cmd", 'python3 "/tmp/odoo-bin" -c "/tmp/odoo.conf"', "--odoo-bin", "/tmp/odoo-bin"])

        with self.assertRaises(SystemExit):
            parse_args(["--base-cmd", 'python3 "/tmp/odoo-bin" -c "/tmp/odoo.conf"', "--config", "/tmp/odoo.conf"])


class CliDispatchTests(unittest.TestCase):
    def test_cli_main_dispatches_verify(self) -> None:
        with patch("tooling.cli.verify_main", return_value=0) as verify_mock:
            result = cli_main(["verify"])

        self.assertEqual(result, 0)
        verify_mock.assert_called_once_with()

    def test_cli_main_dispatches_build(self) -> None:
        with patch("tooling.cli.build_main", return_value=0) as build_mock:
            result = cli_main(["build"])

        self.assertEqual(result, 0)
        build_mock.assert_called_once_with()

    def test_cli_main_dispatches_smoke_install(self) -> None:
        with patch("tooling.cli.smoke_install_main", return_value=0) as smoke_mock:
            result = cli_main(["smoke-install"])

        self.assertEqual(result, 0)
        smoke_mock.assert_called_once_with()

    def test_cli_main_dispatches_install_plugin(self) -> None:
        with patch("tooling.cli.run_install_plugin", return_value=0, create=True) as run_install_plugin_mock:
            try:
                result = cli_main(["install-plugin"])
            except SystemExit as exc:
                self.fail(f"install-plugin subcommand should dispatch, got {exc}")

        self.assertEqual(result, 0)
        run_install_plugin_mock.assert_called_once_with([])

    def test_cli_main_dispatches_install_plugin_uninstall_flag(self) -> None:
        with patch("tooling.cli.run_install_plugin", return_value=0, create=True) as run_install_plugin_mock:
            try:
                result = cli_main(["install-plugin", "--uninstall"])
            except SystemExit as exc:
                self.fail(f"install-plugin --uninstall should dispatch, got {exc}")

        self.assertEqual(result, 0)
        run_install_plugin_mock.assert_called_once_with(["--uninstall"])

    def test_cli_main_dispatches_project_setup(self) -> None:
        argv = [
            "project-setup",
            "--docs-root",
            "/tmp/docs",
            "--source-root",
            "/tmp/src",
            "--version",
            "18.0",
            "--base-cmd",
            'python3 "/tmp/odoo-bin" -c "/tmp/odoo.conf"',
            "--yes",
        ]

        with patch("tooling.cli.run_project_setup", return_value=0) as run_project_setup_mock:
            result = cli_main(argv)

        self.assertEqual(result, 0)
        run_project_setup_mock.assert_called_once()
        dispatched_args = run_project_setup_mock.call_args.args[0]
        self.assertEqual(dispatched_args.command, "project-setup")
        self.assertEqual(dispatched_args.docs_root, "/tmp/docs")
        self.assertEqual(dispatched_args.source_root, "/tmp/src")
        self.assertEqual(dispatched_args.version, "18.0")
        self.assertEqual(dispatched_args.base_cmd, 'python3 "/tmp/odoo-bin" -c "/tmp/odoo.conf"')

    def test_cli_main_rejects_base_cmd_with_odoo_bin_or_config(self) -> None:
        with self.assertRaises(SystemExit):
            cli_main(
                [
                    "project-setup",
                    "--base-cmd",
                    'python3 "/tmp/odoo-bin" -c "/tmp/odoo.conf"',
                    "--odoo-bin",
                    "/tmp/odoo-bin",
                ]
            )

        with self.assertRaises(SystemExit):
            cli_main(
                [
                    "project-setup",
                    "--base-cmd",
                    'python3 "/tmp/odoo-bin" -c "/tmp/odoo.conf"',
                    "--config",
                    "/tmp/odoo.conf",
                ]
            )

    def test_pyproject_exposes_console_scripts(self) -> None:
        pyproject_text = (Path(__file__).resolve().parents[2] / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('odoo-skills = "tooling.cli:main"', pyproject_text)
        self.assertIn('odoo-skills-install = "tooling.install_plugin:main"', pyproject_text)
        self.assertIn('odoo-skills-verify = "tooling.cli:verify_main"', pyproject_text)
        self.assertIn('odoo-skills-build = "tooling.cli:build_main"', pyproject_text)
        self.assertIn('odoo-skills-smoke-install = "tooling.cli:smoke_install_main"', pyproject_text)


class RunProjectSetupTests(unittest.TestCase):
    def test_run_project_setup_rejects_non_odoo_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            args = Namespace(
                docs_root=None,
                source_root=None,
                version=None,
                python_bin=None,
                odoo_bin=None,
                config=None,
                base_cmd=None,
                yes=True,
                force=False,
                dry_run=False,
                command="project-setup",
            )

            with self.assertRaises(SystemExit) as ctx:
                run_project_setup(args, cwd=project_root)

        self.assertIn("does not look like an Odoo project", str(ctx.exception))

    def test_run_project_setup_writes_files_on_first_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / "addons").mkdir()
            docs_root = project_root / "docs"
            source_root = project_root / "src"
            odoo_bin = source_root / "odoo-bin"
            config_path = project_root / "odoo.conf"
            docs_root.mkdir()
            source_root.mkdir()
            odoo_bin.write_text("", encoding="utf-8")
            config_path.write_text("", encoding="utf-8")
            args = Namespace(
                docs_root=str(docs_root),
                source_root=str(source_root),
                version="18.0",
                python_bin="python3",
                odoo_bin=str(odoo_bin),
                config=str(config_path),
                base_cmd=None,
                yes=True,
                force=False,
                dry_run=False,
                command="project-setup",
            )

            result = run_project_setup(args, cwd=project_root)

            settings = json.loads((project_root / ".claude" / "settings.local.json").read_text(encoding="utf-8"))
            state = json.loads((project_root / ".claude" / "odoo-skill-paths.json").read_text(encoding="utf-8"))

        self.assertEqual(result, 0)
        self.assertEqual(
            settings,
            {
                "env": {
                    "ODOO_TEST_BASE_CMD": f'python3 "{odoo_bin}" -c "{config_path}"',
                }
            },
        )
        self.assertEqual(state["docsRoot"], str(docs_root))
        self.assertEqual(state["sourceRoot"], str(source_root))
        self.assertEqual(state["version"], "18.0")
        self.assertEqual(state["majorVersion"], "18")
        self.assertEqual(state["versionSource"], "--version")
        self.assertEqual(state["projectRoot"], str(project_root.resolve()))
        self.assertEqual(state["mode"], "project-setup")
        self.assertIn("configuredAt", state)

    def test_run_project_setup_is_noop_when_existing_state_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / "addons").mkdir()
            docs_root = project_root / "docs"
            source_root = project_root / "src"
            odoo_bin = source_root / "odoo-bin"
            config_path = project_root / "odoo.conf"
            docs_root.mkdir()
            source_root.mkdir()
            odoo_bin.write_text("", encoding="utf-8")
            config_path.write_text("", encoding="utf-8")
            claude_dir = project_root / ".claude"
            claude_dir.mkdir()
            settings_path = claude_dir / "settings.local.json"
            state_path = claude_dir / "odoo-skill-paths.json"
            original_settings = {
                "env": {
                    "KEEP": "value",
                    "ODOO_TEST_BASE_CMD": f'python3 "{odoo_bin}" -c "{config_path}"',
                },
                "other": {"flag": True},
            }
            original_state = {
                "docsRoot": str(docs_root),
                "sourceRoot": str(source_root),
                "version": "18.0",
                "majorVersion": "18",
                "extra": "keep-me",
            }
            settings_path.write_text(json.dumps(original_settings, indent=2) + "\n", encoding="utf-8")
            state_path.write_text(json.dumps(original_state, indent=2) + "\n", encoding="utf-8")
            args = Namespace(
                docs_root=None,
                source_root=None,
                version=None,
                python_bin=None,
                odoo_bin=None,
                config=None,
                base_cmd=None,
                yes=True,
                force=False,
                dry_run=False,
                command="project-setup",
            )

            with patch("builtins.print") as print_mock:
                result = run_project_setup(args, cwd=project_root)

            self.assertEqual(
                json.loads(settings_path.read_text(encoding="utf-8")),
                original_settings,
            )
            self.assertEqual(
                json.loads(state_path.read_text(encoding="utf-8")),
                original_state,
            )

        self.assertEqual(result, 0)
        printed = [call.args[0] for call in print_mock.call_args_list]
        self.assertTrue(any("Project setup already exists" in line for line in printed))

    def test_run_project_setup_force_rewrites_only_managed_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / "addons").mkdir()
            docs_root = project_root / "docs"
            source_root = project_root / "src"
            old_docs_root = project_root / "old-docs"
            old_source_root = project_root / "old-src"
            old_odoo_bin = old_source_root / "odoo-bin"
            old_config_path = project_root / "old.conf"
            odoo_bin = source_root / "odoo-bin"
            config_path = project_root / "odoo.conf"
            docs_root.mkdir()
            source_root.mkdir()
            old_docs_root.mkdir()
            old_source_root.mkdir()
            old_odoo_bin.write_text("", encoding="utf-8")
            old_config_path.write_text("", encoding="utf-8")
            odoo_bin.write_text("", encoding="utf-8")
            config_path.write_text("", encoding="utf-8")
            claude_dir = project_root / ".claude"
            claude_dir.mkdir()
            settings_path = claude_dir / "settings.local.json"
            state_path = claude_dir / "odoo-skill-paths.json"
            settings_path.write_text(
                json.dumps(
                    {
                        "env": {
                            "KEEP": "value",
                            "ODOO_TEST_BASE_CMD": f'python3 "{old_odoo_bin}" -c "{old_config_path}"',
                        },
                        "permissions": {"allow": ["read"]},
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            state_path.write_text(
                json.dumps(
                    {
                        "docsRoot": str(old_docs_root),
                        "sourceRoot": str(old_source_root),
                        "version": "17.0",
                        "majorVersion": "17",
                        "custom": {"keep": True},
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            args = Namespace(
                docs_root=str(docs_root),
                source_root=str(source_root),
                version="19.0",
                python_bin="python3.12",
                odoo_bin=str(odoo_bin),
                config=str(config_path),
                base_cmd=None,
                yes=True,
                force=True,
                dry_run=False,
                command="project-setup",
            )

            result = run_project_setup(args, cwd=project_root)
            settings = json.loads(settings_path.read_text(encoding="utf-8"))
            state = json.loads(state_path.read_text(encoding="utf-8"))

        self.assertEqual(result, 0)
        self.assertEqual(settings["env"]["KEEP"], "value")
        self.assertEqual(settings["permissions"], {"allow": ["read"]})
        self.assertEqual(
            settings["env"]["ODOO_TEST_BASE_CMD"],
            f'python3.12 "{odoo_bin}" -c "{config_path}"',
        )
        self.assertEqual(state["version"], "19.0")
        self.assertEqual(state["majorVersion"], "19")
        self.assertEqual(state["docsRoot"], str(docs_root))
        self.assertEqual(state["sourceRoot"], str(source_root))
        self.assertEqual(state["custom"], {"keep": True})
        self.assertEqual(state["mode"], "project-setup")

    def test_run_project_setup_stale_existing_state_does_not_noop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / "addons").mkdir()
            docs_root = project_root / "docs"
            source_root = project_root / "src"
            odoo_bin = source_root / "odoo-bin"
            config_path = project_root / "odoo.conf"
            docs_root.mkdir()
            source_root.mkdir()
            odoo_bin.write_text("", encoding="utf-8")
            config_path.write_text("", encoding="utf-8")
            claude_dir = project_root / ".claude"
            claude_dir.mkdir()
            settings_path = claude_dir / "settings.local.json"
            state_path = claude_dir / "odoo-skill-paths.json"
            settings_path.write_text(
                json.dumps(
                    {
                        "env": {
                            "ODOO_TEST_BASE_CMD": f'python3 "{odoo_bin}" -c "{config_path}"',
                        }
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            state_path.write_text(
                json.dumps(
                    {
                        "docsRoot": str(project_root / "missing-docs"),
                        "sourceRoot": str(source_root),
                        "version": "18.0",
                        "majorVersion": "18",
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            args = Namespace(
                docs_root=str(docs_root),
                source_root=None,
                version=None,
                python_bin=None,
                odoo_bin=None,
                config=None,
                base_cmd=None,
                yes=True,
                force=False,
                dry_run=False,
                command="project-setup",
            )

            with patch("builtins.print") as print_mock:
                result = run_project_setup(args, cwd=project_root)

            settings = json.loads(settings_path.read_text(encoding="utf-8"))
            state = json.loads(state_path.read_text(encoding="utf-8"))
            printed = [call.args[0] for call in print_mock.call_args_list]

        self.assertEqual(result, 0)
        self.assertEqual(
            settings["env"]["ODOO_TEST_BASE_CMD"],
            f'python3 "{odoo_bin}" -c "{config_path}"',
        )
        self.assertEqual(state["docsRoot"], str(docs_root))
        self.assertEqual(state["sourceRoot"], str(source_root))
        self.assertEqual(state["version"], "18.0")
        self.assertFalse(any("Project setup already exists" in line for line in printed))

    def test_run_project_setup_force_without_python_bin_preserves_saved_interpreter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / "addons").mkdir()
            docs_root = project_root / "docs"
            source_root = project_root / "src"
            old_docs_root = project_root / "old-docs"
            old_source_root = project_root / "old-src"
            odoo_bin = source_root / "odoo-bin"
            config_path = project_root / "odoo.conf"
            old_odoo_bin = old_source_root / "odoo-bin"
            old_config_path = project_root / "old.conf"
            docs_root.mkdir()
            source_root.mkdir()
            old_docs_root.mkdir()
            old_source_root.mkdir()
            odoo_bin.write_text("", encoding="utf-8")
            config_path.write_text("", encoding="utf-8")
            old_odoo_bin.write_text("", encoding="utf-8")
            old_config_path.write_text("", encoding="utf-8")
            claude_dir = project_root / ".claude"
            claude_dir.mkdir()
            settings_path = claude_dir / "settings.local.json"
            state_path = claude_dir / "odoo-skill-paths.json"
            settings_path.write_text(
                json.dumps(
                    {
                        "env": {
                            "ODOO_TEST_BASE_CMD": f'python3.11 "{old_odoo_bin}" -c "{old_config_path}"',
                        }
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            state_path.write_text(
                json.dumps(
                    {
                        "docsRoot": str(old_docs_root),
                        "sourceRoot": str(old_source_root),
                        "version": "17.0",
                        "majorVersion": "17",
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            args = Namespace(
                docs_root=str(docs_root),
                source_root=str(source_root),
                version="18.0",
                python_bin=None,
                odoo_bin=str(odoo_bin),
                config=str(config_path),
                base_cmd=None,
                yes=True,
                force=True,
                dry_run=False,
                command="project-setup",
            )

            result = run_project_setup(args, cwd=project_root)
            settings = json.loads(settings_path.read_text(encoding="utf-8"))

        self.assertEqual(result, 0)
        self.assertEqual(
            settings["env"]["ODOO_TEST_BASE_CMD"],
            f'python3.11 "{odoo_bin}" -c "{config_path}"',
        )

    def test_run_project_setup_dry_run_does_not_write_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / "addons").mkdir()
            docs_root = project_root / "docs"
            source_root = project_root / "src"
            odoo_bin = source_root / "odoo-bin"
            config_path = project_root / "odoo.conf"
            docs_root.mkdir()
            source_root.mkdir()
            odoo_bin.write_text("", encoding="utf-8")
            config_path.write_text("", encoding="utf-8")
            args = Namespace(
                docs_root=str(docs_root),
                source_root=str(source_root),
                version="18.0",
                python_bin="python3",
                odoo_bin=str(odoo_bin),
                config=str(config_path),
                base_cmd=None,
                yes=True,
                force=False,
                dry_run=True,
                command="project-setup",
            )

            with patch("builtins.print") as print_mock:
                result = run_project_setup(args, cwd=project_root)

            printed = [call.args[0] for call in print_mock.call_args_list]

        self.assertEqual(result, 0)
        self.assertTrue(any("Dry run" in line for line in printed))
        self.assertFalse((project_root / ".claude" / "settings.local.json").exists())
        self.assertFalse((project_root / ".claude" / "odoo-skill-paths.json").exists())


if __name__ == "__main__":
    unittest.main()
