#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import os
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Callable, Mapping, Sequence


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
    parser.add_argument("--db", required=True, help="Disposable local database name")
    parser.add_argument("--test-tags", help="Odoo test tags like /sale or module_name")
    parser.add_argument("--install", help="Comma-separated modules to install with -i")
    parser.add_argument("--update", help="Comma-separated modules to update with -u")
    parser.add_argument("--cleanup-before", action="store_true")
    parser.add_argument(
        "--cleanup-after",
        action="store_true",
        help="Deprecated no-op; cleanup after the run is automatic",
    )
    parser.add_argument("--no-stop-after-init", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)



def load_base_command(env: Mapping[str, str] | None = None) -> list[str]:
    source = env or os.environ
    raw = source.get("ODOO_TEST_BASE_CMD", "").strip()
    if not raw:
        raise SystemExit("ODOO_TEST_BASE_CMD is not set")
    return shlex.split(raw)



def extract_config_path(base_argv: Sequence[str]) -> Path:
    for index, token in enumerate(base_argv):
        if token == "-c" and index + 1 < len(base_argv):
            return Path(base_argv[index + 1]).expanduser()
        if token.startswith("--config="):
            return Path(token.split("=", 1)[1]).expanduser()
    raise SystemExit("ODOO_TEST_BASE_CMD must include -c /path/to/odoo.conf or --config=/path/to/odoo.conf")



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



def main(argv: list[str] | None = None, env: Mapping[str, str] | None = None) -> int:
    args = parse_args(argv)
    base_argv = load_base_command(env)
    validate_base_command(base_argv)
    config_path = extract_config_path(base_argv)
    command = build_command(
        base_argv,
        db_name=args.db,
        test_tags=args.test_tags,
        install_modules=args.install,
        update_modules=args.update,
        stop_after_init=not args.no_stop_after_init,
    )

    if not args.dry_run:
        maybe_cleanup(enabled=args.cleanup_before, db_name=args.db, config_path=config_path, dry_run=False)
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
        if not args.dry_run:
            try:
                cleanup_database(
                    db_name=args.db,
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
