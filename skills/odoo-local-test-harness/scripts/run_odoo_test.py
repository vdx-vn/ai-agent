#!/usr/bin/env python3
from __future__ import annotations

import argparse
import configparser
import importlib.util
import os
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Callable, Mapping, Sequence


class MultipleExistingDatabasesError(RuntimeError):
    def __init__(self, candidates: list[str]) -> None:
        self.candidates = candidates
        super().__init__(
            "Multiple existing databases matched the current config: "
            + ", ".join(candidates)
        )


SYSTEM_DATABASES = {"postgres"}


def _load_cleanup_database(module_path: Path | None = None) -> Callable[..., None]:
    cleanup_module_path = module_path or Path(__file__).with_name("delete_unused_odoo_db.py")
    spec = importlib.util.spec_from_file_location("run_odoo_test_cleanup", cleanup_module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load cleanup module from {cleanup_module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    cleanup = getattr(module, "cleanup_database", None)
    if not callable(cleanup):
        raise AttributeError(f"cleanup_database not found in {cleanup_module_path}")
    return cleanup



def cleanup_database(*, db_name: str, config_path: Path, dry_run: bool) -> None:
    delete_unused_cleanup_database = _load_cleanup_database()
    delete_unused_cleanup_database(db_name=db_name, config_path=config_path, dry_run=dry_run)



def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run local Odoo tests from ODOO_TEST_BASE_CMD")
    parser.add_argument("--db", help="Disposable local database name")
    parser.add_argument(
        "--db-mode",
        choices=("auto", "existing", "disposable"),
        default="auto",
        help="Choose whether to use an existing configured DB or a disposable DB",
    )
    parser.add_argument("--test-tags", help="Odoo test tags like /sale or module_name")
    parser.add_argument("--install", help="Comma-separated modules to install with -i")
    parser.add_argument("--update", help="Comma-separated modules to update with -u")
    parser.add_argument("--cleanup-before", action="store_true")
    parser.add_argument(
        "--cleanup-after",
        action="store_true",
        help="Deprecated no-op; cleanup after the run is automatic for disposable DBs",
    )
    parser.add_argument("--no-stop-after-init", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)



def load_base_command(env: Mapping[str, str] | None = None) -> list[str]:
    source = os.environ if env is None else env
    raw = source.get("ODOO_TEST_BASE_CMD", "").strip()
    if not raw:
        raise SystemExit("ODOO_TEST_BASE_CMD is not set")
    return shlex.split(raw)



def extract_config_path(base_argv: Sequence[str]) -> Path:
    for index, token in enumerate(base_argv):
        if token in {"-c", "--config"} and index + 1 < len(base_argv):
            return Path(base_argv[index + 1]).expanduser()
        if token.startswith("--config="):
            return Path(token.split("=", 1)[1]).expanduser()
    raise SystemExit(
        "ODOO_TEST_BASE_CMD must include -c /path/to/odoo.conf, "
        "--config /path/to/odoo.conf, or --config=/path/to/odoo.conf"
    )



def validate_base_command(base_argv: Sequence[str]) -> None:
    inline_prefixes = ("--database=", "--test-tags=", "--init=", "--update=")
    exact_flags = {"-d", "--database", "--test-tags", "-i", "--init", "-u", "--update", "--test-enable", "--stop-after-init"}

    for token in base_argv:
        if token in exact_flags:
            raise SystemExit(
                f"ODOO_TEST_BASE_CMD must not include runtime-managed flag: {token}"
            )
        for prefix in inline_prefixes:
            if token.startswith(prefix):
                raise SystemExit(
                    f"ODOO_TEST_BASE_CMD must not include runtime-managed flag: {prefix}"
                )



def load_config_options(config_path: Path) -> configparser.SectionProxy:
    parser = configparser.ConfigParser()
    if not config_path.exists():
        raise FileNotFoundError(f"Config file does not exist: {config_path}")
    read_files = parser.read(config_path)
    if not read_files:
        raise OSError(f"Could not read config file: {config_path}")
    if not parser.has_section("options"):
        parser.add_section("options")
    return parser["options"]



def _parse_db_name_candidates(raw_db_name: str) -> list[str]:
    normalized = raw_db_name.replace(",", " ")
    return [item.strip() for item in normalized.split() if item.strip()]



def list_accessible_databases(config_path: Path) -> list[str]:
    options = load_config_options(config_path)
    command = [
        "psql",
        "-d",
        "postgres",
        "-Atqc",
        "SELECT datname FROM pg_database WHERE datistemplate = false ORDER BY datname;",
    ]
    for flag, key in (("-h", "db_host"), ("-p", "db_port"), ("-U", "db_user")):
        value = options.get(key, fallback="").strip()
        if value:
            command[1:1] = [flag, value]
    env = None
    db_password = options.get("db_password", fallback="").strip()
    if db_password:
        env = os.environ.copy()
        env["PGPASSWORD"] = db_password
    completed = subprocess.run(command, check=True, capture_output=True, text=True, env=env)
    return [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.strip() and line.strip() not in SYSTEM_DATABASES
    ]



def resolve_existing_db(
    config_path: Path,
    *,
    list_databases: Callable[[Path], list[str]] = list_accessible_databases,
) -> str:
    options = load_config_options(config_path)
    db_name_candidates = _parse_db_name_candidates(options.get("db_name", fallback="").strip())
    if len(db_name_candidates) == 1:
        return db_name_candidates[0]
    if len(db_name_candidates) > 1:
        raise MultipleExistingDatabasesError(db_name_candidates)

    candidates = list_databases(config_path)
    if not candidates:
        raise SystemExit(f"No accessible existing databases found for config: {config_path}")
    if len(candidates) > 1:
        raise MultipleExistingDatabasesError(candidates)
    return candidates[0]



def choose_db_mode(*, requested_mode: str, install_modules: str | None, update_modules: str | None) -> str:
    if requested_mode != "auto":
        return requested_mode
    if install_modules or update_modules:
        return "disposable"
    return "existing"



def build_command(
    base_argv: Sequence[str],
    *,
    db_name: str,
    test_tags: str | None,
    install_modules: str | None,
    update_modules: str | None,
    stop_after_init: bool,
) -> list[str]:
    argv = list(base_argv)
    argv.extend(["-d", db_name])
    if test_tags:
        argv.extend(["--test-tags", test_tags, "--test-enable"])
    if install_modules:
        argv.extend(["-i", install_modules])
    if update_modules:
        argv.extend(["-u", update_modules])
    if stop_after_init and "--stop-after-init" not in argv:
        argv.append("--stop-after-init")
    return argv



def maybe_cleanup(*, enabled: bool, db_name: str, config_path: Path, dry_run: bool) -> None:
    if enabled:
        cleanup_database(db_name=db_name, config_path=config_path, dry_run=dry_run)



def main(
    argv: list[str] | None = None,
    env: Mapping[str, str] | None = None,
    resolve_existing_db_name: Callable[[Path], str] = resolve_existing_db,
) -> int:
    args = parse_args(argv)
    base_argv = load_base_command(env)
    validate_base_command(base_argv)
    config_path = extract_config_path(base_argv)
    db_mode = choose_db_mode(
        requested_mode=args.db_mode,
        install_modules=args.install,
        update_modules=args.update,
    )

    if db_mode == "disposable":
        if not args.db:
            raise SystemExit("--db is required when --db-mode is disposable")
        selected_db = args.db
    elif args.dry_run:
        selected_db = "existing_db"
    else:
        selected_db = resolve_existing_db_name(config_path)

    command = build_command(
        base_argv,
        db_name=selected_db,
        test_tags=args.test_tags,
        install_modules=args.install,
        update_modules=args.update,
        stop_after_init=not args.no_stop_after_init,
    )

    cleanup_enabled = db_mode == "disposable"
    if cleanup_enabled and not args.dry_run:
        maybe_cleanup(enabled=args.cleanup_before, db_name=selected_db, config_path=config_path, dry_run=False)
    print("Resolved config path:", config_path)
    print("Selected mode:", db_mode)
    print("Selected DB:", selected_db)
    print("Resolved base command:", " ".join(shlex.quote(part) for part in base_argv))
    print("Final command:", " ".join(shlex.quote(part) for part in command))

    primary_error: BaseException | None = None
    try:
        if args.dry_run:
            return 0

        subprocess.run(command, check=True)
        return 0
    except BaseException as exc:
        primary_error = exc
        raise
    finally:
        if cleanup_enabled and not args.dry_run:
            try:
                cleanup_database(
                    db_name=selected_db,
                    config_path=config_path,
                    dry_run=False,
                )
            except Exception as cleanup_exc:
                if primary_error is None:
                    raise
                if isinstance(primary_error, Exception):
                    print(f"Cleanup failed after primary error: {cleanup_exc}", file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
