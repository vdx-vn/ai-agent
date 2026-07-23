import json
import subprocess
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch

from tooling.cli import main as cli_main
from tooling.local_setup_common import repo_looks_odoo, resolve_project_root
from tooling.project_setup import _find_extra_addons_candidate, run_project_setup


class ProjectRootHelpersTests(unittest.TestCase):
    def test_repo_looks_odoo_accepts_manifest_near_repo_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            addon_dir = repo_root / "sale_ext"
            addon_dir.mkdir()
            (addon_dir / "__manifest__.py").write_text("{}\n", encoding="utf-8")

            self.assertTrue(repo_looks_odoo(repo_root))

    def test_project_setup_accepts_cwd_that_is_addons_dir_even_if_git_root_is_not_odoo(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            git_root = Path(tmp) / "repo"
            extra_addons = git_root / "sources" / "extra-addons"
            extra_addons.mkdir(parents=True)
            (extra_addons / "my_addon" / "__manifest__.py").parent.mkdir()
            (extra_addons / "my_addon" / "__manifest__.py").write_text("{}\n", encoding="utf-8")

            self.assertFalse(repo_looks_odoo(git_root))
            self.assertTrue(repo_looks_odoo(extra_addons))

    def test_find_extra_addons_candidate_finds_nested_extra_addons(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            git_root = Path(tmp) / "repo"
            extra_addons = git_root / "sources" / "extra-addons"
            extra_addons.mkdir(parents=True)

            result = _find_extra_addons_candidate(git_root, git_root)

            self.assertEqual(result, extra_addons)

    def test_find_extra_addons_candidate_prefers_start_dir_child(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            git_root = Path(tmp) / "repo"
            start_dir = git_root / "sources"
            local_extra = start_dir / "extra-addons"
            local_extra.mkdir(parents=True)
            nested_extra = git_root / "other" / "extra-addons"
            nested_extra.mkdir(parents=True)

            result = _find_extra_addons_candidate(git_root, start_dir)

            self.assertEqual(result, local_extra)

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
                yes=True,
                force=False,
                dry_run=False,
                command="project-setup",
            )

            with self.assertRaises(SystemExit) as ctx:
                run_project_setup(args, cwd=project_root)

        self.assertIn("does not look like an Odoo project", str(ctx.exception))

    def test_run_project_setup_is_noop_when_existing_state_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / "addons").mkdir()
            docs_root = project_root / "docs"
            source_root = project_root / "src"
            docs_root.mkdir()
            source_root.mkdir()
            claude_dir = project_root / ".claude"
            claude_dir.mkdir()
            state_path = claude_dir / "odoo-skill-paths.json"
            shared_path = project_root / ".odoo-skills" / "project.json"
            original_state = {
                "docsRoot": str(docs_root),
                "sourceRoot": str(source_root),
                "version": "18.0",
                "majorVersion": "18",
                "extra": "keep-me",
            }
            state_path.write_text(json.dumps(original_state, indent=2) + "\n", encoding="utf-8")
            shared_path.parent.mkdir()
            shared_path.write_text(json.dumps(original_state, indent=2) + "\n", encoding="utf-8")
            args = Namespace(
                docs_root=None,
                source_root=None,
                version=None,
                yes=True,
                force=False,
                dry_run=False,
                command="project-setup",
            )

            with patch("builtins.print") as print_mock:
                result = run_project_setup(args, cwd=project_root)

            self.assertEqual(
                json.loads(state_path.read_text(encoding="utf-8")),
                original_state,
            )
            self.assertEqual(
                json.loads(shared_path.read_text(encoding="utf-8")),
                original_state,
            )

        self.assertEqual(result, 0)
        printed = [call.args[0] for call in print_mock.call_args_list]
        self.assertTrue(any("Project setup already exists" in line for line in printed))

    def test_run_project_setup_stale_existing_state_does_not_noop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / "addons").mkdir()
            docs_root = project_root / "docs"
            source_root = project_root / "src"
            docs_root.mkdir()
            source_root.mkdir()
            claude_dir = project_root / ".claude"
            claude_dir.mkdir()
            state_path = claude_dir / "odoo-skill-paths.json"
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
                yes=True,
                force=False,
                dry_run=False,
                command="project-setup",
            )

            with patch("builtins.print") as print_mock:
                result = run_project_setup(args, cwd=project_root)

            state = json.loads(state_path.read_text(encoding="utf-8"))
            printed = [call.args[0] for call in print_mock.call_args_list]

        self.assertEqual(result, 0)
        self.assertEqual(state["docsRoot"], str(docs_root))
        self.assertEqual(state["sourceRoot"], str(source_root))
        self.assertEqual(state["version"], "18.0")
        self.assertFalse(any("Project setup already exists" in line for line in printed))

    def test_run_project_setup_dry_run_does_not_write_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / "addons").mkdir()
            docs_root = project_root / "docs"
            source_root = project_root / "src"
            docs_root.mkdir()
            source_root.mkdir()
            args = Namespace(
                docs_root=str(docs_root),
                source_root=str(source_root),
                version="18.0",
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
        self.assertFalse((project_root / ".claude" / "odoo-skill-paths.json").exists())
        self.assertFalse((project_root / ".odoo-skills" / "project.json").exists())


if __name__ == "__main__":
    unittest.main()
