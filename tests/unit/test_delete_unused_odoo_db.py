import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

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
import delete_unused_odoo_db as cleanup  # type: ignore


class DeleteUnusedOdooDbTests(unittest.TestCase):
    def test_resolve_data_dir_prefers_config_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            conf = Path(tmp) / "odoo.conf"
            conf.write_text("[options]\ndata_dir = /srv/odoo-data\n")
            self.assertEqual(cleanup.resolve_data_dir(conf, Path("/home/test")), Path("/srv/odoo-data"))

    def test_cleanup_database_terminates_connections_drops_db_and_removes_filestore(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            conf = Path(tmp) / "odoo.conf"
            data_dir = Path(tmp) / "data"
            filestore = data_dir / "filestore" / "tmp_odoo_test"
            filestore.mkdir(parents=True)
            conf.write_text(f"[options]\ndata_dir = {data_dir}\n")

            run_calls = []
            removed = []
            terminate_sql = (
                "SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
                "WHERE datname = 'tmp_odoo_test' AND pid <> pg_backend_pid();"
            )

            cleanup.cleanup_database(
                db_name="tmp_odoo_test",
                config_path=conf,
                dry_run=False,
                run_command=lambda cmd, check, env=None: run_calls.append((cmd, check, env)),
                remove_tree=lambda path: removed.append(path),
            )

            self.assertEqual(
                run_calls,
                [
                    (["psql", "-d", "postgres", "-Atqc", terminate_sql], True, None),
                    (["dropdb", "--if-exists", "tmp_odoo_test"], True, None),
                ],
            )
            self.assertEqual(removed, [filestore.resolve()])

    def test_cleanup_database_uses_home_fallback_when_data_dir_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            conf = Path(tmp) / "odoo.conf"
            conf.write_text("[options]\n")
            self.assertEqual(
                cleanup.filestore_path(conf, "tmp_odoo_test", Path("/home/test")),
                Path("/home/test/.local/share/Odoo/filestore/tmp_odoo_test"),
            )

    def test_cleanup_database_stops_when_terminate_sessions_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            conf = Path(tmp) / "odoo.conf"
            data_dir = Path(tmp) / "data"
            filestore = data_dir / "filestore" / "tmp_odoo_test"
            filestore.mkdir(parents=True)
            conf.write_text(f"[options]\ndata_dir = {data_dir}\n")

            run_calls = []
            removed = []

            def fake_run(cmd, check, env=None):
                run_calls.append((cmd, check, env))
                raise subprocess.CalledProcessError(returncode=1, cmd=cmd)

            with self.assertRaises(subprocess.CalledProcessError):
                cleanup.cleanup_database(
                    db_name="tmp_odoo_test",
                    config_path=conf,
                    dry_run=False,
                    run_command=fake_run,
                    remove_tree=lambda path: removed.append(path),
                )

            self.assertEqual(len(run_calls), 1)
            self.assertEqual(run_calls[0][0][:4], ["psql", "-d", "postgres", "-Atqc"])
            self.assertEqual(removed, [])

    def test_cleanup_database_skips_filestore_delete_when_dropdb_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            conf = Path(tmp) / "odoo.conf"
            data_dir = Path(tmp) / "data"
            filestore = data_dir / "filestore" / "tmp_odoo_test"
            filestore.mkdir(parents=True)
            conf.write_text(f"[options]\ndata_dir = {data_dir}\n")

            run_calls = []
            removed = []

            def fake_run(cmd, check, env=None):
                run_calls.append((cmd, check, env))
                if cmd[0] == "dropdb":
                    raise subprocess.CalledProcessError(returncode=1, cmd=cmd)

            with self.assertRaises(subprocess.CalledProcessError):
                cleanup.cleanup_database(
                    db_name="tmp_odoo_test",
                    config_path=conf,
                    dry_run=False,
                    run_command=fake_run,
                    remove_tree=lambda path: removed.append(path),
                )

            self.assertEqual(len(run_calls), 2)
            self.assertEqual(run_calls[0][0][:4], ["psql", "-d", "postgres", "-Atqc"])
            self.assertEqual(run_calls[1][0][:2], ["dropdb", "--if-exists"])
            self.assertEqual(removed, [])

    def test_cleanup_database_uses_configured_db_connection_settings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            conf = Path(tmp) / "odoo.conf"
            data_dir = Path(tmp) / "data"
            filestore = data_dir / "filestore" / "tmp_odoo_test"
            filestore.mkdir(parents=True)
            conf.write_text(
                "[options]\n"
                f"data_dir = {data_dir}\n"
                "db_host = localhost\n"
                "db_port = 5432\n"
                "db_user = qms\n"
                "db_password = qms\n"
            )

            run_calls = []
            terminate_sql = (
                "SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
                "WHERE datname = 'tmp_odoo_test' AND pid <> pg_backend_pid();"
            )

            def fake_run(cmd, check, env=None):
                run_calls.append((cmd, check, env))

            cleanup.cleanup_database(
                db_name="tmp_odoo_test",
                config_path=conf,
                dry_run=False,
                run_command=fake_run,
                remove_tree=lambda path: None,
            )

            self.assertEqual(len(run_calls), 2)
            terminate_cmd, terminate_check, terminate_env = run_calls[0]
            self.assertEqual(
                terminate_cmd,
                [
                    "psql",
                    "-U",
                    "qms",
                    "-p",
                    "5432",
                    "-h",
                    "localhost",
                    "-d",
                    "postgres",
                    "-Atqc",
                    terminate_sql,
                ],
            )
            self.assertTrue(terminate_check)
            self.assertIsNotNone(terminate_env)
            self.assertEqual(terminate_env["PGPASSWORD"], "qms")

            dropdb_cmd, dropdb_check, dropdb_env = run_calls[1]
            self.assertEqual(
                dropdb_cmd,
                [
                    "dropdb",
                    "--if-exists",
                    "-h",
                    "localhost",
                    "-p",
                    "5432",
                    "-U",
                    "qms",
                    "tmp_odoo_test",
                ],
            )
            self.assertTrue(dropdb_check)
            self.assertIsNotNone(dropdb_env)
            self.assertEqual(dropdb_env["PGPASSWORD"], "qms")

    def test_validate_db_name_rejects_invalid_values(self) -> None:
        for db_name in ["", "   ", ".", "..", "foo/bar", "foo\\bar", "/tmp/evil"]:
            with self.subTest(db_name=db_name):
                with self.assertRaises(ValueError):
                    cleanup.validate_db_name(db_name)

    def test_cleanup_database_dry_run_skips_dropdb_and_remove_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            conf = Path(tmp) / "odoo.conf"
            data_dir = Path(tmp) / "data"
            conf.write_text(f"[options]\ndata_dir = {data_dir}\n")

            run_calls = []
            removed = []

            cleanup.cleanup_database(
                db_name="tmp_odoo_test",
                config_path=conf,
                dry_run=True,
                run_command=lambda cmd, check: run_calls.append((cmd, check)),
                remove_tree=lambda path: removed.append(path),
            )

            self.assertEqual(run_calls, [])
            self.assertEqual(removed, [])

    def test_resolve_data_dir_rejects_missing_config_file(self) -> None:
        missing = Path(tempfile.gettempdir()) / "missing-odoo.conf"
        with self.assertRaises(FileNotFoundError):
            cleanup.resolve_data_dir(missing)


if __name__ == "__main__":
    unittest.main()
