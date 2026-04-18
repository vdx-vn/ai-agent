import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import call, patch

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
    def test_main_runs_cleanup_before_and_after(self, run_mock, cleanup_mock) -> None:
        exit_code = run_odoo_test.main(
            [
                "--db",
                "tmp_odoo_test",
                "--test-tags",
                "/sale",
                "--cleanup-before",
                "--cleanup-after",
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
    @patch("run_odoo_test.subprocess.run", side_effect=subprocess.CalledProcessError(returncode=1, cmd=["odoo"]))
    def test_main_runs_cleanup_after_when_subprocess_fails(self, run_mock, cleanup_mock) -> None:
        with self.assertRaises(subprocess.CalledProcessError):
            run_odoo_test.main(
                [
                    "--db",
                    "tmp_odoo_test",
                    "--cleanup-after",
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

    @patch("run_odoo_test.cleanup_database")
    @patch("run_odoo_test.subprocess.run")
    def test_main_dry_run_skips_cleanup_and_subprocess(self, run_mock, cleanup_mock) -> None:
        exit_code = run_odoo_test.main(
            [
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


if __name__ == "__main__":
    unittest.main()
