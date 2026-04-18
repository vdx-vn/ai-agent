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

    def test_cleanup_database_drops_db_and_removes_filestore(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            conf = Path(tmp) / "odoo.conf"
            data_dir = Path(tmp) / "data"
            filestore = data_dir / "filestore" / "tmp_odoo_test"
            filestore.mkdir(parents=True)
            conf.write_text(f"[options]\ndata_dir = {data_dir}\n")

            run_calls = []
            removed = []

            cleanup.cleanup_database(
                db_name="tmp_odoo_test",
                config_path=conf,
                dry_run=False,
                run_command=lambda cmd, check: run_calls.append((cmd, check)),
                remove_tree=lambda path: removed.append(path),
            )

            self.assertEqual(run_calls, [(["dropdb", "--if-exists", "tmp_odoo_test"], True)])
            self.assertEqual(removed, [filestore.resolve()])

    def test_cleanup_database_uses_home_fallback_when_data_dir_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            conf = Path(tmp) / "odoo.conf"
            conf.write_text("[options]\n")
            self.assertEqual(
                cleanup.filestore_path(conf, "tmp_odoo_test", Path("/home/test")),
                Path("/home/test/.local/share/Odoo/filestore/tmp_odoo_test"),
            )

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
