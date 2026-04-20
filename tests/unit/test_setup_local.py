import json
import subprocess
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import call, patch

from tooling.setup_local import (
    SetupInputs,
    add_marketplace,
    build_base_cmd,
    collect_setup_inputs,
    main,
    merge_settings_local,
    parse_args,
    remove_managed_settings,
    restore_materialized_files,
    run_command,
    run_setup,
    run_uninstall,
    validate_base_cmd,
)


class ParseArgsTests(unittest.TestCase):
    def test_parse_args_supports_setup_local_options(self) -> None:
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
                "python /tmp/odoo-bin -c /tmp/odoo.conf",
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
        self.assertEqual(args.base_cmd, "python /tmp/odoo-bin -c /tmp/odoo.conf")
        self.assertTrue(args.yes)
        self.assertTrue(args.uninstall)

    def test_parse_args_defaults_python_bin_to_python3(self) -> None:
        args = parse_args([])

        self.assertEqual(args.python_bin, "python3")
        self.assertFalse(args.yes)
        self.assertFalse(args.uninstall)


class BaseCommandTests(unittest.TestCase):
    def test_build_base_cmd_constructs_python_odoo_and_config_command(self) -> None:
        command = build_base_cmd("python3.11", "/opt/odoo/odoo-bin", "/etc/odoo.conf")

        self.assertEqual(command, 'python3.11 "/opt/odoo/odoo-bin" -c "/etc/odoo.conf"')

    def test_validate_base_cmd_accepts_config_short_flag(self) -> None:
        command = validate_base_cmd('python3 "/opt/odoo/odoo-bin" -c "/etc/odoo.conf"')

        self.assertEqual(command, 'python3 "/opt/odoo/odoo-bin" -c "/etc/odoo.conf"')

    def test_validate_base_cmd_accepts_config_long_flag(self) -> None:
        command = validate_base_cmd('python3 "/opt/odoo/odoo-bin" --config /etc/odoo.conf')

        self.assertEqual(command, 'python3 "/opt/odoo/odoo-bin" --config /etc/odoo.conf')

    def test_validate_base_cmd_rejects_missing_config_flag(self) -> None:
        with self.assertRaises(SystemExit) as ctx:
            validate_base_cmd('python3 "/opt/odoo/odoo-bin"')

        self.assertIn("-c", str(ctx.exception))
        self.assertIn("--config", str(ctx.exception))

    def test_validate_base_cmd_rejects_malformed_quoted_command(self) -> None:
        with self.assertRaises(SystemExit) as ctx:
            validate_base_cmd('python3 "/opt/odoo/odoo-bin -c /etc/odoo.conf')

        self.assertIn("ODOO_TEST_BASE_CMD is not a valid shell command", str(ctx.exception))

    def test_validate_base_cmd_rejects_runtime_managed_short_flags(self) -> None:
        for forbidden in ["-d", "-i", "-u"]:
            with self.subTest(forbidden=forbidden):
                with self.assertRaises(SystemExit) as ctx:
                    validate_base_cmd(f'python3 "/opt/odoo/odoo-bin" -c /etc/odoo.conf {forbidden} demo')

                self.assertIn(forbidden, str(ctx.exception))

    def test_validate_base_cmd_rejects_runtime_managed_attached_short_flags(self) -> None:
        cases = [
            ("-ddemo", "-d"),
            ("-isale", "-i"),
            ("-ucrm", "-u"),
        ]
        for token, forbidden in cases:
            with self.subTest(token=token):
                with self.assertRaises(SystemExit) as ctx:
                    validate_base_cmd(f'python3 "/opt/odoo/odoo-bin" -c /etc/odoo.conf {token}')

                self.assertIn(forbidden, str(ctx.exception))

    def test_validate_base_cmd_rejects_runtime_managed_long_flags(self) -> None:
        for forbidden in ["--test-tags", "--test-enable", "--stop-after-init"]:
            with self.subTest(forbidden=forbidden):
                with self.assertRaises(SystemExit) as ctx:
                    validate_base_cmd(f'python3 "/opt/odoo/odoo-bin" --config /etc/odoo.conf {forbidden}')

                self.assertIn(forbidden, str(ctx.exception))


class RestoreMaterializedFilesTests(unittest.TestCase):
    def test_restore_materialized_files_restores_backed_up_contents_without_git(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            managed_file = repo_root / ".claude" / "skills" / "demo" / "SKILL.md"
            managed_file.parent.mkdir(parents=True, exist_ok=True)
            managed_file.write_text("materialized\n", encoding="utf-8")

            restore_materialized_files(
                repo_root,
                [str(managed_file)],
                {str(managed_file): "local edits\n"},
            )

            restored = managed_file.read_text(encoding="utf-8")

        self.assertEqual(restored, "local edits\n")

    def test_restore_materialized_files_preserves_file_when_no_backup_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            managed_file = repo_root / ".claude" / "skills" / "demo" / "SKILL.md"
            managed_file.parent.mkdir(parents=True, exist_ok=True)
            managed_file.write_text("user changes\n", encoding="utf-8")

            restore_materialized_files(repo_root, [str(managed_file)], {})

            restored = managed_file.read_text(encoding="utf-8")

        self.assertEqual(restored, "user changes\n")


class SettingsHelpersTests(unittest.TestCase):
    def test_merge_settings_local_updates_only_managed_env_key(self) -> None:
        existing = {
            "permissions": {"allow": ["Read"]},
            "env": {
                "KEEP": "value",
                "ODOO_TEST_BASE_CMD": "old",
            },
            "hooks": {"SessionStart": []},
        }

        merged = merge_settings_local(existing, 'python3 "/tmp/odoo-bin" -c "/tmp/odoo.conf"')

        self.assertEqual(merged["permissions"], existing["permissions"])
        self.assertEqual(merged["hooks"], existing["hooks"])
        self.assertEqual(merged["env"]["KEEP"], "value")
        self.assertEqual(
            merged["env"]["ODOO_TEST_BASE_CMD"],
            'python3 "/tmp/odoo-bin" -c "/tmp/odoo.conf"',
        )

    def test_remove_managed_settings_removes_nested_env_keys_only(self) -> None:
        existing = {
            "env": {"ODOO_TEST_BASE_CMD": "old", "KEEP": "value"},
            "permissions": {"allow": ["Read"]},
        }

        cleaned = remove_managed_settings(existing, {"env": ["ODOO_TEST_BASE_CMD"]})

        self.assertEqual(cleaned, {"env": {"KEEP": "value"}, "permissions": {"allow": ["Read"]}})


class CollectSetupInputsTests(unittest.TestCase):
    def test_collect_setup_inputs_prompts_for_missing_values_when_interactive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            docs_root = repo_root / "docs"
            source_root = repo_root / "src"
            odoo_bin = repo_root / "odoo-bin"
            config_path = repo_root / "odoo.conf"
            docs_root.mkdir()
            source_root.mkdir()
            odoo_bin.write_text("", encoding="utf-8")
            config_path.write_text("", encoding="utf-8")
            args = Namespace(
                docs_root=None,
                source_root=None,
                version=None,
                python_bin="python3",
                odoo_bin=None,
                config=None,
                base_cmd=None,
                yes=False,
                uninstall=False,
            )

            with patch("tooling.local_setup_common.resolve_series", side_effect=SystemExit("no detection")):
                with patch(
                    "builtins.input",
                    side_effect=[
                        str(docs_root),
                        str(source_root),
                        "18.0",
                        str(odoo_bin),
                        str(config_path),
                    ],
                ):
                    result = collect_setup_inputs(repo_root, args)

        self.assertEqual(
            result,
            SetupInputs(
                docs_root=docs_root,
                source_root=source_root,
                version="18.0",
                python_bin="python3",
                odoo_bin=odoo_bin,
                config_path=config_path,
                base_cmd=f'python3 "{odoo_bin}" -c "{config_path}"',
                yes=False,
                uninstall=False,
            ),
        )

    def test_collect_setup_inputs_raises_in_yes_mode_when_required_values_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            args = Namespace(
                docs_root=None,
                source_root=None,
                version=None,
                python_bin="python3",
                odoo_bin=None,
                config=None,
                base_cmd=None,
                yes=True,
                uninstall=False,
            )

            with self.assertRaises(SystemExit) as ctx:
                collect_setup_inputs(repo_root, args)

        self.assertIn("--docs-root", str(ctx.exception))

    def test_collect_setup_inputs_uses_provided_base_cmd_directly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            docs_root = repo_root / "docs"
            source_root = repo_root / "src"
            docs_root.mkdir()
            source_root.mkdir()
            args = Namespace(
                docs_root=str(docs_root),
                source_root=str(source_root),
                version=None,
                python_bin="python3",
                odoo_bin=None,
                config=None,
                base_cmd='python3 "/opt/odoo/odoo-bin" -c "/etc/odoo.conf"',
                yes=True,
                uninstall=False,
            )

            with patch("tooling.setup_local._resolve_version_or_prompt", return_value=("18.0", "detected")):
                result = collect_setup_inputs(repo_root, args)

        self.assertEqual(result.base_cmd, 'python3 "/opt/odoo/odoo-bin" -c "/etc/odoo.conf"')
        self.assertIsNone(result.odoo_bin)
        self.assertIsNone(result.config_path)
        self.assertEqual(result.version, "18.0")

    def test_collect_setup_inputs_rejects_relative_docs_and_source_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            docs_root = repo_root / "docs"
            source_root = repo_root / "src"
            docs_root.mkdir()
            source_root.mkdir()
            args = Namespace(
                docs_root="docs",
                source_root="src",
                version="18.0",
                python_bin="python3",
                odoo_bin=None,
                config=None,
                base_cmd="custom command",
                yes=True,
                uninstall=False,
            )

            with self.assertRaises(SystemExit) as ctx:
                collect_setup_inputs(repo_root, args)

        self.assertIn("absolute", str(ctx.exception).lower())
        self.assertIn("--docs-root", str(ctx.exception))

    def test_collect_setup_inputs_rejects_file_for_docs_and_source_roots(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            docs_root = repo_root / "docs"
            source_root = repo_root / "src"
            docs_root.write_text("not a directory", encoding="utf-8")
            source_root.mkdir()
            args = Namespace(
                docs_root=str(docs_root),
                source_root=str(source_root),
                version="18.0",
                python_bin="python3",
                odoo_bin=None,
                config=None,
                base_cmd="custom command",
                yes=True,
                uninstall=False,
            )

            with self.assertRaises(SystemExit) as ctx:
                collect_setup_inputs(repo_root, args)

        self.assertIn("directory", str(ctx.exception).lower())
        self.assertIn("--docs-root", str(ctx.exception))

    def test_collect_setup_inputs_rejects_directory_for_odoo_bin_and_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            docs_root = repo_root / "docs"
            source_root = repo_root / "src"
            odoo_bin = repo_root / "odoo-bin"
            config_path = repo_root / "odoo.conf"
            docs_root.mkdir()
            source_root.mkdir()
            odoo_bin.mkdir()
            config_path.mkdir()
            args = Namespace(
                docs_root=str(docs_root),
                source_root=str(source_root),
                version="18.0",
                python_bin="python3",
                odoo_bin=str(odoo_bin),
                config=str(config_path),
                base_cmd=None,
                yes=True,
                uninstall=False,
            )

            with self.assertRaises(SystemExit) as ctx:
                collect_setup_inputs(repo_root, args)

        self.assertIn("file", str(ctx.exception).lower())
        self.assertIn("--odoo-bin", str(ctx.exception))


class RunCommandTests(unittest.TestCase):
    def test_run_command_captures_output_and_returns_completed_process(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            with patch("tooling.setup_local.subprocess.run") as subprocess_run_mock:
                expected = subprocess.CompletedProcess(["cmd"], 0, stdout="ok\n", stderr="warn\n")
                subprocess_run_mock.return_value = expected

                result = run_command(repo_root, ["cmd"])

        self.assertIs(result, expected)
        subprocess_run_mock.assert_called_once_with(
            ["cmd"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )


class SetupOrchestrationTests(unittest.TestCase):
    def test_run_setup_writes_local_state_and_calls_claude_commands_in_order(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            settings_path = repo_root / ".claude" / "settings.local.json"
            state_path = repo_root / ".claude" / "odoo-skill-paths.json"
            settings_path.parent.mkdir(parents=True, exist_ok=True)
            settings_path.write_text(json.dumps({"env": {"KEEP": "value"}}, indent=2) + "\n", encoding="utf-8")
            args = Namespace(
                docs_root=str(repo_root / "docs"),
                source_root=str(repo_root / "src"),
                version="18.0",
                python_bin="python3",
                odoo_bin=str(repo_root / "odoo-bin"),
                config=str(repo_root / "odoo.conf"),
                base_cmd=None,
                yes=True,
                uninstall=False,
            )
            setup_inputs = SetupInputs(
                docs_root=repo_root / "docs",
                source_root=repo_root / "src",
                version="18.0",
                python_bin="python3",
                odoo_bin=repo_root / "odoo-bin",
                config_path=repo_root / "odoo.conf",
                base_cmd='python3 "/tmp/odoo-bin" -c "/tmp/odoo.conf"',
                yes=True,
                uninstall=False,
            )
            marketplace_path = repo_root / "dist" / "marketplace"
            materialized_result = type("Result", (), {"materialized_files": [repo_root / ".claude" / "skills" / "a" / "SKILL.md"]})()
            events: list[str] = []

            def record_write_json_file(path: Path, payload: dict[str, object]) -> None:
                if path == settings_path:
                    events.append("settings write")
                elif path == state_path and "setupCompletedAt" in payload:
                    events.append("final setupCompletedAt write")
                elif path == state_path:
                    events.append("metadata/state write")
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

            def record_materialize_skills(**kwargs: object) -> object:
                events.append("materialize")
                return materialized_result

            def record_build_marketplace(build_repo_root: Path, build_marketplace_path: Path) -> Path:
                self.assertEqual(build_repo_root, repo_root)
                self.assertEqual(build_marketplace_path, marketplace_path)
                events.append("build")
                return marketplace_path

            def record_run_command(_repo_root: Path, command: list[str]) -> None:
                if command[:3] == ["claude", "plugin", "validate"]:
                    events.append("validate")
                elif command[:3] == ["claude", "plugin", "install"]:
                    events.append("install")

            def record_add_marketplace(add_repo_root: Path, built_marketplace: Path) -> None:
                self.assertEqual(add_repo_root, repo_root)
                self.assertEqual(built_marketplace, marketplace_path)
                events.append("add_marketplace")

            with patch("tooling.setup_local.collect_setup_inputs", return_value=setup_inputs):
                with patch("tooling.setup_local.ensure_claude_cli") as ensure_mock:
                    with patch("tooling.setup_local.write_json_file", side_effect=record_write_json_file):
                        with patch("tooling.setup_local.materialize_skills", side_effect=record_materialize_skills) as materialize_mock:
                            with patch("tooling.setup_local.build_marketplace", side_effect=record_build_marketplace) as build_mock:
                                with patch("tooling.setup_local.add_marketplace", side_effect=record_add_marketplace) as add_marketplace_mock:
                                    with patch("tooling.setup_local.run_command", side_effect=record_run_command) as run_command_mock:
                                        with patch("builtins.print") as print_mock:
                                            result = run_setup(repo_root, args)

            saved_settings = json.loads(settings_path.read_text(encoding="utf-8"))
            saved_state = json.loads(state_path.read_text(encoding="utf-8"))
            printed_lines = [args[0] for args, _kwargs in print_mock.call_args_list]

        self.assertEqual(result, 0)
        ensure_mock.assert_called_once_with()
        materialize_mock.assert_called_once()
        materialize_kwargs = materialize_mock.call_args.kwargs
        self.assertEqual(materialize_kwargs["docs_root"], setup_inputs.docs_root)
        self.assertEqual(materialize_kwargs["source_root"], setup_inputs.source_root)
        self.assertEqual(materialize_kwargs["version"], "18.0")
        self.assertEqual(materialize_kwargs["skills_root"], repo_root / ".claude" / "skills")
        self.assertEqual(materialize_kwargs["config_path"], state_path)
        self.assertEqual(
            materialize_kwargs["extra_metadata"],
            {
                "managedSettings": {"env": ["ODOO_TEST_BASE_CMD"]},
                "pluginName": "odoo-skills",
                "marketplaceName": "odoo-skills-dev",
                "installScope": "local",
                "marketplacePath": str(marketplace_path),
            },
        )
        build_mock.assert_called_once_with(repo_root, marketplace_path)
        add_marketplace_mock.assert_called_once_with(repo_root, marketplace_path)
        self.assertEqual(
            run_command_mock.call_args_list,
            [
                call(repo_root, ["claude", "plugin", "validate", str(marketplace_path)]),
                call(repo_root, ["claude", "plugin", "install", "odoo-skills@odoo-skills-dev", "--scope", "local"]),
            ],
        )
        self.assertEqual(
            events,
            [
                "settings write",
                "materialize",
                "build",
                "metadata/state write",
                "validate",
                "add_marketplace",
                "install",
                "final setupCompletedAt write",
            ],
        )
        self.assertEqual(saved_settings["env"]["KEEP"], "value")
        self.assertEqual(saved_settings["env"]["ODOO_TEST_BASE_CMD"], setup_inputs.base_cmd)
        self.assertEqual(saved_state["managedSettings"], {"env": ["ODOO_TEST_BASE_CMD"]})
        self.assertEqual(saved_state["pluginName"], "odoo-skills")
        self.assertEqual(saved_state["marketplaceName"], "odoo-skills-dev")
        self.assertEqual(saved_state["installScope"], "local")
        self.assertEqual(saved_state["marketplacePath"], str(marketplace_path))
        self.assertIn("setupCompletedAt", saved_state)
        self.assertTrue(any("Setup complete" in line for line in printed_lines))
        self.assertTrue(any("--uninstall" in line for line in printed_lines))

    def test_add_marketplace_retries_remove_and_add_when_existing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            marketplace_path = repo_root / "dist" / "marketplace"
            add_command = ["claude", "plugin", "marketplace", "add", str(marketplace_path)]
            existing_error = subprocess.CalledProcessError(
                1,
                add_command,
                stderr="Marketplace odoo-skills-dev already exists\n",
            )

            with patch("tooling.setup_local.run_command", side_effect=[existing_error, None, None]) as run_command_mock:
                add_marketplace(repo_root, marketplace_path)

        self.assertEqual(
            run_command_mock.call_args_list,
            [
                call(repo_root, add_command),
                call(repo_root, ["claude", "plugin", "marketplace", "remove", "odoo-skills-dev"]),
                call(repo_root, add_command),
            ],
        )

    def test_add_marketplace_reraises_non_existing_called_process_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            marketplace_path = repo_root / "dist" / "marketplace"
            add_command = ["claude", "plugin", "marketplace", "add", str(marketplace_path)]
            failure = subprocess.CalledProcessError(1, add_command, stderr="permission denied\n")

            with patch("tooling.setup_local.run_command", side_effect=failure) as run_command_mock:
                with self.assertRaises(subprocess.CalledProcessError):
                    add_marketplace(repo_root, marketplace_path)

        run_command_mock.assert_called_once_with(repo_root, add_command)

    def test_run_setup_restores_previous_settings_materialized_files_and_marketplace_on_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            settings_path = repo_root / ".claude" / "settings.local.json"
            settings_path.parent.mkdir(parents=True, exist_ok=True)
            original_settings = {"env": {"KEEP": "value"}}
            settings_path.write_text(json.dumps(original_settings, indent=2) + "\n", encoding="utf-8")
            state_path = repo_root / ".claude" / "odoo-skill-paths.json"
            marketplace_path = repo_root / "dist" / "marketplace"
            marketplace_path.mkdir(parents=True, exist_ok=True)
            args = Namespace(
                docs_root=str(repo_root / "docs"),
                source_root=str(repo_root / "src"),
                version="18.0",
                python_bin="python3",
                odoo_bin=str(repo_root / "odoo-bin"),
                config=str(repo_root / "odoo.conf"),
                base_cmd=None,
                yes=True,
                uninstall=False,
            )
            setup_inputs = SetupInputs(
                docs_root=repo_root / "docs",
                source_root=repo_root / "src",
                version="18.0",
                python_bin="python3",
                odoo_bin=repo_root / "odoo-bin",
                config_path=repo_root / "odoo.conf",
                base_cmd='python3 "/tmp/odoo-bin" -c "/tmp/odoo.conf"',
                yes=True,
                uninstall=False,
            )
            materialized_files = [str(repo_root / ".claude" / "skills" / "demo" / "SKILL.md")]
            materialized_result = type("Result", (), {"materialized_files": materialized_files})()

            with patch("tooling.setup_local.collect_setup_inputs", return_value=setup_inputs):
                with patch("tooling.setup_local.ensure_claude_cli"):
                    with patch("tooling.setup_local.materialize_skills", return_value=materialized_result):
                        with patch("tooling.setup_local.build_marketplace", return_value=marketplace_path):
                            with patch("tooling.setup_local.restore_materialized_files") as restore_mock:
                                with patch("tooling.setup_local.add_marketplace", side_effect=RuntimeError("install failed")):
                                    with patch("tooling.setup_local.run_command"):
                                        with self.assertRaisesRegex(RuntimeError, "install failed"):
                                            run_setup(repo_root, args)

            restored_settings = json.loads(settings_path.read_text(encoding="utf-8"))

        self.assertEqual(restored_settings, original_settings)
        restore_mock.assert_called_once_with(repo_root, materialized_files, {})
        self.assertFalse(marketplace_path.exists())
        self.assertFalse(state_path.exists())

    def test_run_setup_removes_created_settings_state_and_marketplace_on_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            settings_path = repo_root / ".claude" / "settings.local.json"
            state_path = repo_root / ".claude" / "odoo-skill-paths.json"
            marketplace_path = repo_root / "dist" / "marketplace"
            marketplace_path.mkdir(parents=True, exist_ok=True)
            args = Namespace(
                docs_root=str(repo_root / "docs"),
                source_root=str(repo_root / "src"),
                version="18.0",
                python_bin="python3",
                odoo_bin=str(repo_root / "odoo-bin"),
                config=str(repo_root / "odoo.conf"),
                base_cmd=None,
                yes=True,
                uninstall=False,
            )
            setup_inputs = SetupInputs(
                docs_root=repo_root / "docs",
                source_root=repo_root / "src",
                version="18.0",
                python_bin="python3",
                odoo_bin=repo_root / "odoo-bin",
                config_path=repo_root / "odoo.conf",
                base_cmd='python3 "/tmp/odoo-bin" -c "/tmp/odoo.conf"',
                yes=True,
                uninstall=False,
            )
            materialized_files = [str(repo_root / ".claude" / "skills" / "demo" / "SKILL.md")]
            materialized_result = type("Result", (), {"materialized_files": materialized_files})()

            with patch("tooling.setup_local.collect_setup_inputs", return_value=setup_inputs):
                with patch("tooling.setup_local.ensure_claude_cli"):
                    with patch("tooling.setup_local.materialize_skills", return_value=materialized_result):
                        with patch("tooling.setup_local.build_marketplace", return_value=marketplace_path):
                            with patch("tooling.setup_local.restore_materialized_files") as restore_mock:
                                with patch("tooling.setup_local.add_marketplace", side_effect=RuntimeError("install failed")):
                                    with patch("tooling.setup_local.run_command"):
                                        with self.assertRaisesRegex(RuntimeError, "install failed"):
                                            run_setup(repo_root, args)

        restore_mock.assert_called_once_with(repo_root, materialized_files, {})
        self.assertFalse(settings_path.exists())
        self.assertFalse(state_path.exists())
        self.assertFalse(marketplace_path.exists())

    def test_run_setup_removes_marketplace_on_rollback_after_successful_marketplace_add(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            marketplace_path = repo_root / "dist" / "marketplace"
            marketplace_path.mkdir(parents=True, exist_ok=True)
            args = Namespace(
                docs_root=str(repo_root / "docs"),
                source_root=str(repo_root / "src"),
                version="18.0",
                python_bin="python3",
                odoo_bin=str(repo_root / "odoo-bin"),
                config=str(repo_root / "odoo.conf"),
                base_cmd=None,
                yes=True,
                uninstall=False,
            )
            setup_inputs = SetupInputs(
                docs_root=repo_root / "docs",
                source_root=repo_root / "src",
                version="18.0",
                python_bin="python3",
                odoo_bin=repo_root / "odoo-bin",
                config_path=repo_root / "odoo.conf",
                base_cmd='python3 "/tmp/odoo-bin" -c "/tmp/odoo.conf"',
                yes=True,
                uninstall=False,
            )
            materialized_result = type("Result", (), {"materialized_files": []})()
            failure = RuntimeError("install failed")

            with patch("tooling.setup_local.collect_setup_inputs", return_value=setup_inputs):
                with patch("tooling.setup_local.ensure_claude_cli"):
                    with patch("tooling.setup_local.materialize_skills", return_value=materialized_result):
                        with patch("tooling.setup_local.build_marketplace", return_value=marketplace_path):
                            with patch("tooling.setup_local.add_marketplace") as add_marketplace_mock:
                                with patch("tooling.setup_local.run_command") as run_command_mock:
                                    run_command_mock.side_effect = [None, failure, None]
                                    with self.assertRaisesRegex(RuntimeError, "install failed"):
                                        run_setup(repo_root, args)

        add_marketplace_mock.assert_called_once_with(repo_root, marketplace_path)
        self.assertEqual(
            run_command_mock.call_args_list,
            [
                call(repo_root, ["claude", "plugin", "validate", str(marketplace_path)]),
                call(repo_root, ["claude", "plugin", "install", "odoo-skills@odoo-skills-dev", "--scope", "local"]),
                call(repo_root, ["claude", "plugin", "marketplace", "remove", "odoo-skills-dev"]),
            ],
        )

    def test_run_setup_uninstalls_plugin_on_rollback_after_successful_plugin_install(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            marketplace_path = repo_root / "dist" / "marketplace"
            marketplace_path.mkdir(parents=True, exist_ok=True)
            args = Namespace(
                docs_root=str(repo_root / "docs"),
                source_root=str(repo_root / "src"),
                version="18.0",
                python_bin="python3",
                odoo_bin=str(repo_root / "odoo-bin"),
                config=str(repo_root / "odoo.conf"),
                base_cmd=None,
                yes=True,
                uninstall=False,
            )
            setup_inputs = SetupInputs(
                docs_root=repo_root / "docs",
                source_root=repo_root / "src",
                version="18.0",
                python_bin="python3",
                odoo_bin=repo_root / "odoo-bin",
                config_path=repo_root / "odoo.conf",
                base_cmd='python3 "/tmp/odoo-bin" -c "/tmp/odoo.conf"',
                yes=True,
                uninstall=False,
            )
            materialized_result = type("Result", (), {"materialized_files": []})()
            failure = RuntimeError("state write failed")

            with patch("tooling.setup_local.collect_setup_inputs", return_value=setup_inputs):
                with patch("tooling.setup_local.ensure_claude_cli"):
                    with patch("tooling.setup_local.materialize_skills", return_value=materialized_result):
                        with patch("tooling.setup_local.build_marketplace", return_value=marketplace_path):
                            with patch("tooling.setup_local.add_marketplace") as add_marketplace_mock:
                                with patch("tooling.setup_local.update_setup_state") as update_state_mock:
                                    update_state_mock.side_effect = [
                                        {"marketplaceName": "odoo-skills-dev", "pluginName": "odoo-skills", "installScope": "local"},
                                        failure,
                                    ]
                                    with patch("tooling.setup_local.run_command") as run_command_mock:
                                        with self.assertRaisesRegex(RuntimeError, "state write failed"):
                                            run_setup(repo_root, args)

        add_marketplace_mock.assert_called_once_with(repo_root, marketplace_path)
        self.assertEqual(
            run_command_mock.call_args_list,
            [
                call(repo_root, ["claude", "plugin", "validate", str(marketplace_path)]),
                call(repo_root, ["claude", "plugin", "install", "odoo-skills@odoo-skills-dev", "--scope", "local"]),
                call(repo_root, ["claude", "plugin", "uninstall", "odoo-skills", "--scope", "local"]),
                call(repo_root, ["claude", "plugin", "marketplace", "remove", "odoo-skills-dev"]),
            ],
        )

    def test_run_uninstall_skips_external_claude_commands_when_state_file_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            settings_path = repo_root / ".claude" / "settings.local.json"
            settings_path.parent.mkdir(parents=True, exist_ok=True)
            settings_path.write_text(
                json.dumps({"env": {"ODOO_TEST_BASE_CMD": "cmd", "KEEP": "value"}}, indent=2) + "\n",
                encoding="utf-8",
            )
            args = Namespace(uninstall=True)

            with patch("tooling.setup_local.ensure_claude_cli") as ensure_mock:
                ensure_mock.return_value = True
                with patch("tooling.setup_local.run_command") as run_command_mock:
                    with patch("tooling.setup_local.restore_materialized_files") as restore_mock:
                        result = run_uninstall(repo_root, args)

            saved_settings = json.loads(settings_path.read_text(encoding="utf-8"))

        self.assertEqual(result, 0)
        ensure_mock.assert_not_called()
        run_command_mock.assert_not_called()
        restore_mock.assert_not_called()
        self.assertEqual(saved_settings, {"env": {"KEEP": "value"}})

    def test_run_uninstall_skips_external_claude_commands_when_state_is_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            state_path = repo_root / ".claude" / "odoo-skill-paths.json"
            state_path.parent.mkdir(parents=True, exist_ok=True)
            state_path.write_text("{}\n", encoding="utf-8")
            settings_path = repo_root / ".claude" / "settings.local.json"
            settings_path.write_text(
                json.dumps({"env": {"ODOO_TEST_BASE_CMD": "cmd", "KEEP": "value"}}, indent=2) + "\n",
                encoding="utf-8",
            )
            args = Namespace(uninstall=True)

            with patch("tooling.setup_local.ensure_claude_cli") as ensure_mock:
                ensure_mock.return_value = True
                with patch("tooling.setup_local.run_command") as run_command_mock:
                    with patch("tooling.setup_local.restore_materialized_files") as restore_mock:
                        result = run_uninstall(repo_root, args)

            saved_settings = json.loads(settings_path.read_text(encoding="utf-8"))

        self.assertEqual(result, 0)
        ensure_mock.assert_not_called()
        run_command_mock.assert_not_called()
        restore_mock.assert_not_called()
        self.assertEqual(saved_settings, {"env": {"KEEP": "value"}})
        self.assertFalse(state_path.exists())

    def test_run_uninstall_continues_when_settings_local_is_malformed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            managed_file = repo_root / "skills" / "demo" / "SKILL.md"
            managed_file.parent.mkdir(parents=True, exist_ok=True)
            managed_file.write_text("materialized\n", encoding="utf-8")
            settings_path = repo_root / ".claude" / "settings.local.json"
            settings_path.parent.mkdir(parents=True, exist_ok=True)
            settings_path.write_text("{not-json\n", encoding="utf-8")
            marketplace_path = repo_root / "dist" / "marketplace"
            marketplace_path.mkdir(parents=True, exist_ok=True)
            state_path = repo_root / ".claude" / "odoo-skill-paths.json"
            state_path.write_text(
                json.dumps(
                    {
                        "materializedFiles": [str(managed_file)],
                        "managedSettings": {"env": ["ODOO_TEST_BASE_CMD"]},
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            args = Namespace(uninstall=True)

            with patch("tooling.setup_local.ensure_claude_cli", return_value=False):
                with patch("tooling.setup_local.restore_materialized_files") as restore_mock:
                    result = run_uninstall(repo_root, args)

        self.assertEqual(result, 0)
        restore_mock.assert_called_once_with(repo_root, [str(managed_file)], {})
        self.assertFalse(settings_path.exists())
        self.assertFalse(marketplace_path.exists())
        self.assertFalse(state_path.exists())

    def test_run_uninstall_restores_recorded_file_and_cleans_managed_settings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            managed_file = repo_root / "skills" / "demo" / "SKILL.md"
            managed_file.parent.mkdir(parents=True, exist_ok=True)
            managed_file.write_text("materialized\n", encoding="utf-8")
            settings_path = repo_root / ".claude" / "settings.local.json"
            settings_path.parent.mkdir(parents=True, exist_ok=True)
            settings_path.write_text(
                json.dumps({"env": {"ODOO_TEST_BASE_CMD": "cmd", "KEEP": "value"}}, indent=2) + "\n",
                encoding="utf-8",
            )
            marketplace_path = repo_root / "dist" / "marketplace"
            marketplace_path.mkdir(parents=True, exist_ok=True)
            state_path = repo_root / ".claude" / "odoo-skill-paths.json"
            state_path.write_text(
                json.dumps(
                    {
                        "materializedFiles": [str(managed_file)],
                        "managedSettings": {"env": ["ODOO_TEST_BASE_CMD"]},
                        "pluginName": "odoo-skills",
                        "installScope": "local",
                        "marketplaceName": "odoo-skills-dev",
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            args = Namespace(uninstall=True)

            with patch("tooling.setup_local.ensure_claude_cli") as ensure_mock:
                ensure_mock.return_value = True
                with patch("tooling.setup_local.run_command") as run_command_mock:
                    with patch("tooling.setup_local.restore_materialized_files") as restore_mock:
                        result = run_uninstall(repo_root, args)

            saved_settings = json.loads(settings_path.read_text(encoding="utf-8"))

        self.assertEqual(result, 0)
        ensure_mock.assert_called_once_with(required=False)
        self.assertEqual(
            run_command_mock.call_args_list,
            [
                call(repo_root, ["claude", "plugin", "uninstall", "odoo-skills", "--scope", "local"]),
                call(repo_root, ["claude", "plugin", "marketplace", "remove", "odoo-skills-dev"]),
            ],
        )
        restore_mock.assert_called_once_with(repo_root, [str(managed_file)], {})
        self.assertEqual(saved_settings, {"env": {"KEEP": "value"}})
        self.assertFalse(marketplace_path.exists())
        self.assertFalse(state_path.exists())

    def test_run_uninstall_continues_local_cleanup_when_claude_commands_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            managed_file = repo_root / "skills" / "demo" / "SKILL.md"
            managed_file.parent.mkdir(parents=True, exist_ok=True)
            managed_file.write_text("materialized\n", encoding="utf-8")
            settings_path = repo_root / ".claude" / "settings.local.json"
            settings_path.parent.mkdir(parents=True, exist_ok=True)
            settings_path.write_text(
                json.dumps({"env": {"ODOO_TEST_BASE_CMD": "cmd", "KEEP": "value"}}, indent=2) + "\n",
                encoding="utf-8",
            )
            marketplace_path = repo_root / "dist" / "marketplace"
            marketplace_path.mkdir(parents=True, exist_ok=True)
            state_path = repo_root / ".claude" / "odoo-skill-paths.json"
            state_path.write_text(
                json.dumps(
                    {
                        "materializedFiles": [str(managed_file)],
                        "managedSettings": {"env": ["ODOO_TEST_BASE_CMD"]},
                        "pluginName": "odoo-skills",
                        "installScope": "local",
                        "marketplaceName": "odoo-skills-dev",
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            args = Namespace(uninstall=True)
            failure = subprocess.CalledProcessError(1, ["claude"], stderr="missing plugin\n")

            with patch("tooling.setup_local.ensure_claude_cli") as ensure_mock:
                ensure_mock.return_value = True
                with patch("tooling.setup_local.run_command", side_effect=[failure, failure]) as run_command_mock:
                    with patch("tooling.setup_local.restore_materialized_files") as restore_mock:
                        result = run_uninstall(repo_root, args)

            saved_settings = json.loads(settings_path.read_text(encoding="utf-8"))

        self.assertEqual(result, 0)
        ensure_mock.assert_called_once_with(required=False)
        self.assertEqual(run_command_mock.call_count, 2)
        restore_mock.assert_called_once_with(repo_root, [str(managed_file)], {})
        self.assertEqual(saved_settings, {"env": {"KEEP": "value"}})
        self.assertFalse(marketplace_path.exists())
        self.assertFalse(state_path.exists())


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
