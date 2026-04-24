import io
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import call, patch

sys.dont_write_bytecode = True

sys.path.insert(
    0,
    str(
        Path(__file__).resolve().parents[2]
        / "skills"
        / "odoo-local-test-harness"
        / "scripts"
    ),
)
import run_odoo_test  # type: ignore


class RunOdooTestTests(unittest.TestCase):
    def test_choose_db_mode_auto_uses_existing_when_no_install_or_update(self) -> None:
        self.assertEqual(
            run_odoo_test.choose_db_mode(
                requested_mode="auto",
                install_modules=None,
                update_modules=None,
            ),
            "existing",
        )

    def test_choose_db_mode_auto_uses_disposable_when_install_present(self) -> None:
        self.assertEqual(
            run_odoo_test.choose_db_mode(
                requested_mode="auto",
                install_modules="sale",
                update_modules=None,
            ),
            "disposable",
        )

    def test_choose_db_mode_auto_uses_disposable_when_update_present(self) -> None:
        self.assertEqual(
            run_odoo_test.choose_db_mode(
                requested_mode="auto",
                install_modules=None,
                update_modules="stock",
            ),
            "disposable",
        )

    def test_resolve_existing_db_uses_config_db_name_when_present(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "odoo.conf"
            config_path.write_text("[options]\ndb_name = existing_db\n")

            self.assertEqual(
                run_odoo_test.resolve_existing_db(
                    config_path,
                    list_databases=lambda _path: ["fallback_db"],
                ),
                "existing_db",
            )

    def test_resolve_existing_db_falls_back_to_accessible_db_list_when_db_name_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "odoo.conf"
            config_path.write_text("[options]\ndb_host = localhost\n")

            self.assertEqual(
                run_odoo_test.resolve_existing_db(
                    config_path,
                    list_databases=lambda _path: ["accessible_db"],
                ),
                "accessible_db",
            )

    def test_resolve_existing_db_raises_with_candidates_when_multiple_databases_match(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "odoo.conf"
            config_path.write_text("[options]\ndb_host = localhost\n")

            with self.assertRaises(run_odoo_test.MultipleExistingDatabasesError) as exc:
                run_odoo_test.resolve_existing_db(
                    config_path,
                    list_databases=lambda _path: ["db_one", "db_two"],
                )

        self.assertEqual(exc.exception.candidates, ["db_one", "db_two"])
        self.assertIn("db_one", str(exc.exception))
        self.assertIn("db_two", str(exc.exception))

    def test_resolve_existing_db_raises_when_config_lists_multiple_db_names(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "odoo.conf"
            config_path.write_text("[options]\ndb_name = db_one, db_two\n")

            with self.assertRaises(run_odoo_test.MultipleExistingDatabasesError) as exc:
                run_odoo_test.resolve_existing_db(
                    config_path,
                    list_databases=lambda _path: ["fallback_db"],
                )

        self.assertEqual(exc.exception.candidates, ["db_one", "db_two"])

    @patch("run_odoo_test.cleanup_database")
    @patch("run_odoo_test.subprocess.run")
    def test_main_existing_mode_skips_cleanup_before_and_after(self, run_mock, cleanup_mock) -> None:
        exit_code = run_odoo_test.main(
            [
                "--db-mode",
                "existing",
                "--cleanup-before",
            ],
            env={
                "ODOO_TEST_BASE_CMD": "python3 /opt/odoo/odoo-bin -c /tmp/odoo.conf"
            },
            resolve_existing_db_name=lambda _config_path: "existing_db",
        )

        self.assertEqual(exit_code, 0)
        cleanup_mock.assert_not_called()
        run_mock.assert_called_once_with(
            [
                "python3",
                "/opt/odoo/odoo-bin",
                "-c",
                "/tmp/odoo.conf",
                "-d",
                "existing_db",
                "--stop-after-init",
            ],
            check=True,
        )

    @patch("run_odoo_test.cleanup_database")
    @patch("run_odoo_test.subprocess.run")
    def test_main_disposable_mode_keeps_cleanup_before_and_after(self, run_mock, cleanup_mock) -> None:
        exit_code = run_odoo_test.main(
            [
                "--db-mode",
                "disposable",
                "--db",
                "tmp_odoo_test",
                "--cleanup-before",
            ],
            env={
                "ODOO_TEST_BASE_CMD": "python3 /opt/odoo/odoo-bin -c /tmp/odoo.conf"
            },
        )

        self.assertEqual(exit_code, 0)
        cleanup_mock.assert_has_calls(
            [
                call(db_name="tmp_odoo_test", config_path=Path("/tmp/odoo.conf"), dry_run=False),
                call(db_name="tmp_odoo_test", config_path=Path("/tmp/odoo.conf"), dry_run=False),
            ]
        )
        self.assertEqual(cleanup_mock.call_count, 2)
        run_mock.assert_called_once_with(
            [
                "python3",
                "/opt/odoo/odoo-bin",
                "-c",
                "/tmp/odoo.conf",
                "-d",
                "tmp_odoo_test",
                "--stop-after-init",
            ],
            check=True,
        )

    def test_build_command_appends_local_runtime_flags(self) -> None:
        command = run_odoo_test.build_command(
            ["python3", "/opt/odoo/odoo-bin", "-c", "/tmp/odoo.conf"],
            db_name="tmp_odoo_test",
            test_tags="/sale",
            install_modules="sale",
            update_modules="stock",
            stop_after_init=True,
        )
        self.assertEqual(
            command,
            [
                "python3",
                "/opt/odoo/odoo-bin",
                "-c",
                "/tmp/odoo.conf",
                "-d",
                "tmp_odoo_test",
                "--test-tags",
                "/sale",
                "--test-enable",
                "-i",
                "sale",
                "-u",
                "stock",
                "--stop-after-init",
            ],
        )

    def test_extract_config_path_supports_long_form_space_separated_flag(self) -> None:
        self.assertEqual(
            run_odoo_test.extract_config_path(
                [
                    "python3",
                    "/opt/odoo/odoo-bin",
                    "--config",
                    "/tmp/odoo.conf",
                ]
            ),
            Path("/tmp/odoo.conf"),
        )

    @patch("run_odoo_test.cleanup_database")
    @patch("run_odoo_test.subprocess.run")
    def test_main_accepts_long_form_space_separated_config_flag(self, run_mock, cleanup_mock) -> None:
        exit_code = run_odoo_test.main(
            [
                "--db-mode",
                "existing",
            ],
            env={
                "ODOO_TEST_BASE_CMD": "python3 /opt/odoo/odoo-bin --config /tmp/odoo.conf"
            },
            resolve_existing_db_name=lambda _config_path: "existing_db",
        )

        self.assertEqual(exit_code, 0)
        cleanup_mock.assert_not_called()
        run_mock.assert_called_once_with(
            [
                "python3",
                "/opt/odoo/odoo-bin",
                "--config",
                "/tmp/odoo.conf",
                "-d",
                "existing_db",
                "--stop-after-init",
            ],
            check=True,
        )

    def test_validate_base_command_rejects_managed_flags(self) -> None:
        cases = [
            (["python3", "odoo-bin", "-c", "/tmp/odoo.conf", "-d", "db"], "-d"),
            (["python3", "odoo-bin", "-c", "/tmp/odoo.conf", "--database", "db"], "--database"),
            (["python3", "odoo-bin", "-c", "/tmp/odoo.conf", "--database=mydb"], "--database="),
            (["python3", "odoo-bin", "-c", "/tmp/odoo.conf", "--test-tags", "/sale"], "--test-tags"),
            (["python3", "odoo-bin", "-c", "/tmp/odoo.conf", "--test-tags=/sale"], "--test-tags="),
            (["python3", "odoo-bin", "-c", "/tmp/odoo.conf", "-i", "sale"], "-i"),
            (["python3", "odoo-bin", "-c", "/tmp/odoo.conf", "--init", "sale"], "--init"),
            (["python3", "odoo-bin", "-c", "/tmp/odoo.conf", "--init=sale"], "--init="),
            (["python3", "odoo-bin", "-c", "/tmp/odoo.conf", "-u", "sale"], "-u"),
            (["python3", "odoo-bin", "-c", "/tmp/odoo.conf", "--update", "sale"], "--update"),
            (["python3", "odoo-bin", "-c", "/tmp/odoo.conf", "--update=sale"], "--update="),
            (["python3", "odoo-bin", "-c", "/tmp/odoo.conf", "--test-enable"], "--test-enable"),
            (["python3", "odoo-bin", "-c", "/tmp/odoo.conf", "--stop-after-init"], "--stop-after-init"),
        ]

        for base_argv, flag in cases:
            with self.subTest(flag=flag):
                with self.assertRaises(SystemExit) as exc:
                    run_odoo_test.validate_base_command(base_argv)
                self.assertIn("ODOO_TEST_BASE_CMD must not include runtime-managed flag", str(exc.exception))
                self.assertIn(flag, str(exc.exception))

    def test_main_rejects_runtime_managed_flags_in_base_command(self) -> None:
        with self.assertRaises(SystemExit) as exc:
            run_odoo_test.main(
                ["--db", "tmp_odoo_test"],
                env={
                    "ODOO_TEST_BASE_CMD": "python3 /opt/odoo/odoo-bin -c /tmp/odoo.conf --stop-after-init"
                },
            )

        self.assertIn("ODOO_TEST_BASE_CMD must not include runtime-managed flag: --stop-after-init", str(exc.exception))

    def test_load_base_command_requires_env(self) -> None:
        with self.assertRaises(SystemExit) as exc:
            run_odoo_test.load_base_command({})
        self.assertIn("ODOO_TEST_BASE_CMD is not set", str(exc.exception))

    def test_load_cleanup_database_from_explicit_module_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            module_path = Path(temp_dir) / "delete_unused_odoo_db.py"
            module_path.write_text(
                textwrap.dedent(
                    """
                    def cleanup_database(*, db_name, config_path, dry_run):
                        return {
                            "db_name": db_name,
                            "config_path": str(config_path),
                            "dry_run": dry_run,
                        }
                    """
                )
            )

            cleanup = run_odoo_test._load_cleanup_database(module_path)

            result = cleanup(
                db_name="tmp_odoo_test",
                config_path=Path("/tmp/odoo.conf"),
                dry_run=True,
            )

        self.assertEqual(
            result,
            {
                "db_name": "tmp_odoo_test",
                "config_path": "/tmp/odoo.conf",
                "dry_run": True,
            },
        )

    @patch("run_odoo_test.cleanup_database")
    @patch("run_odoo_test.subprocess.run")
    def test_main_runs_automatic_cleanup_after_success(self, run_mock, cleanup_mock) -> None:
        exit_code = run_odoo_test.main(
            [
                "--db-mode",
                "disposable",
                "--db",
                "tmp_odoo_test",
                "--test-tags",
                "/sale",
            ],
            env={
                "ODOO_TEST_BASE_CMD": "python3 /opt/odoo/odoo-bin -c /tmp/odoo.conf"
            },
        )

        self.assertEqual(exit_code, 0)
        cleanup_mock.assert_called_once_with(
            db_name="tmp_odoo_test",
            config_path=Path("/tmp/odoo.conf"),
            dry_run=False,
        )
        run_mock.assert_called_once_with(
            [
                "python3",
                "/opt/odoo/odoo-bin",
                "-c",
                "/tmp/odoo.conf",
                "-d",
                "tmp_odoo_test",
                "--test-tags",
                "/sale",
                "--test-enable",
                "--stop-after-init",
            ],
            check=True,
        )

    @patch("run_odoo_test.cleanup_database")
    @patch("run_odoo_test.subprocess.run")
    def test_main_runs_cleanup_before_and_automatic_after(self, run_mock, cleanup_mock) -> None:
        exit_code = run_odoo_test.main(
            [
                "--db-mode",
                "disposable",
                "--db",
                "tmp_odoo_test",
                "--cleanup-before",
            ],
            env={
                "ODOO_TEST_BASE_CMD": "python3 /opt/odoo/odoo-bin -c /tmp/odoo.conf"
            },
        )

        self.assertEqual(exit_code, 0)
        cleanup_mock.assert_has_calls(
            [
                call(db_name="tmp_odoo_test", config_path=Path("/tmp/odoo.conf"), dry_run=False),
                call(db_name="tmp_odoo_test", config_path=Path("/tmp/odoo.conf"), dry_run=False),
            ]
        )
        self.assertEqual(cleanup_mock.call_count, 2)
        run_mock.assert_called_once_with(
            [
                "python3",
                "/opt/odoo/odoo-bin",
                "-c",
                "/tmp/odoo.conf",
                "-d",
                "tmp_odoo_test",
                "--stop-after-init",
            ],
            check=True,
        )

    @patch("run_odoo_test.cleanup_database")
    @patch("run_odoo_test.subprocess.run", side_effect=subprocess.CalledProcessError(returncode=1, cmd=["odoo"]))
    def test_main_runs_cleanup_after_when_subprocess_fails(self, run_mock, cleanup_mock) -> None:
        with self.assertRaises(subprocess.CalledProcessError):
            run_odoo_test.main(
                [
                    "--db-mode",
                    "disposable",
                    "--db",
                    "tmp_odoo_test",
                ],
                env={
                    "ODOO_TEST_BASE_CMD": "python3 /opt/odoo/odoo-bin -c /tmp/odoo.conf"
                },
            )

        cleanup_mock.assert_called_once_with(
            db_name="tmp_odoo_test",
            config_path=Path("/tmp/odoo.conf"),
            dry_run=False,
        )
        run_mock.assert_called_once()

    @patch("run_odoo_test.cleanup_database", side_effect=RuntimeError("cleanup failed"))
    @patch("run_odoo_test.subprocess.run", side_effect=subprocess.CalledProcessError(returncode=1, cmd=["odoo"]))
    def test_main_preserves_subprocess_error_when_cleanup_also_fails(self, run_mock, cleanup_mock) -> None:
        stderr = io.StringIO()

        with patch("sys.stderr", stderr):
            with self.assertRaises(subprocess.CalledProcessError):
                run_odoo_test.main(
                    [
                        "--db-mode",
                        "disposable",
                        "--db",
                        "tmp_odoo_test",
                    ],
                    env={
                        "ODOO_TEST_BASE_CMD": "python3 /opt/odoo/odoo-bin -c /tmp/odoo.conf"
                    },
                )

        self.assertIn("cleanup failed", stderr.getvalue())
        cleanup_mock.assert_called_once_with(
            db_name="tmp_odoo_test",
            config_path=Path("/tmp/odoo.conf"),
            dry_run=False,
        )
        run_mock.assert_called_once()

    @patch("run_odoo_test.cleanup_database", side_effect=RuntimeError("cleanup failed"))
    @patch("run_odoo_test.subprocess.run", side_effect=KeyboardInterrupt())
    def test_main_preserves_keyboard_interrupt_when_cleanup_also_fails(self, run_mock, cleanup_mock) -> None:
        with self.assertRaises(KeyboardInterrupt):
            run_odoo_test.main(
                [
                    "--db-mode",
                    "disposable",
                    "--db",
                    "tmp_odoo_test",
                ],
                env={
                    "ODOO_TEST_BASE_CMD": "python3 /opt/odoo/odoo-bin -c /tmp/odoo.conf"
                },
            )

        cleanup_mock.assert_called_once_with(
            db_name="tmp_odoo_test",
            config_path=Path("/tmp/odoo.conf"),
            dry_run=False,
        )
        run_mock.assert_called_once()

    @patch("run_odoo_test.cleanup_database", side_effect=RuntimeError("cleanup failed"))
    @patch("run_odoo_test.subprocess.run")
    def test_main_surfaces_cleanup_error_when_subprocess_succeeds(self, run_mock, cleanup_mock) -> None:
        with self.assertRaises(RuntimeError) as exc:
            run_odoo_test.main(
                [
                    "--db-mode",
                    "disposable",
                    "--db",
                    "tmp_odoo_test",
                ],
                env={
                    "ODOO_TEST_BASE_CMD": "python3 /opt/odoo/odoo-bin -c /tmp/odoo.conf"
                },
            )

        self.assertIn("cleanup failed", str(exc.exception))
        cleanup_mock.assert_called_once_with(
            db_name="tmp_odoo_test",
            config_path=Path("/tmp/odoo.conf"),
            dry_run=False,
        )
        run_mock.assert_called_once_with(
            [
                "python3",
                "/opt/odoo/odoo-bin",
                "-c",
                "/tmp/odoo.conf",
                "-d",
                "tmp_odoo_test",
                "--stop-after-init",
            ],
            check=True,
        )

    @patch("run_odoo_test.cleanup_database")
    @patch("run_odoo_test.subprocess.run")
    def test_main_dry_run_skips_cleanup_and_subprocess(self, run_mock, cleanup_mock) -> None:
        exit_code = run_odoo_test.main(
            [
                "--db-mode",
                "disposable",
                "--db",
                "tmp_odoo_test",
                "--test-tags",
                "/sale",
                "--cleanup-before",
                "--cleanup-after",
                "--dry-run",
            ],
            env={
                "ODOO_TEST_BASE_CMD": "python3 /opt/odoo/odoo-bin -c /tmp/odoo.conf"
            },
        )

        self.assertEqual(exit_code, 0)
        cleanup_mock.assert_not_called()
        run_mock.assert_not_called()

    @patch("run_odoo_test.cleanup_database")
    @patch("run_odoo_test.subprocess.run")
    def test_main_existing_mode_dry_run_does_not_require_config_file(self, run_mock, cleanup_mock) -> None:
        exit_code = run_odoo_test.main(
            [
                "--db-mode",
                "existing",
                "--dry-run",
            ],
            env={
                "ODOO_TEST_BASE_CMD": "python3 /opt/odoo/odoo-bin -c /tmp/does-not-exist.conf"
            },
        )

        self.assertEqual(exit_code, 0)
        cleanup_mock.assert_not_called()
        run_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
