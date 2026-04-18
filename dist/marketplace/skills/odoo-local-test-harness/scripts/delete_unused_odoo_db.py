#!/usr/bin/env python3
from __future__ import annotations

import argparse
import configparser
import re
import shutil
import subprocess
from pathlib import Path
from typing import Callable


DB_NAME_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+$")



def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Delete local Odoo database and matching filestore")
    parser.add_argument("--db", required=True, help="Database to delete")
    parser.add_argument("--config", required=True, help="Odoo config path with optional data_dir")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)



def validate_db_name(db_name: str) -> str:
    normalized = db_name.strip()
    if not normalized:
        raise ValueError("db_name is required")
    if normalized in {".", ".."}:
        raise ValueError(f"Invalid db_name: {db_name!r}")
    if Path(normalized).is_absolute() or "/" in normalized or "\\" in normalized:
        raise ValueError(f"Invalid db_name: {db_name!r}")
    if not DB_NAME_PATTERN.fullmatch(normalized):
        raise ValueError(f"Invalid db_name: {db_name!r}")
    return normalized



def resolve_data_dir(config_path: Path, home_path: Path | None = None) -> Path:
    parser = configparser.ConfigParser()
    if not config_path.exists():
        raise FileNotFoundError(f"Config file does not exist: {config_path}")
    read_files = parser.read(config_path)
    if not read_files:
        raise OSError(f"Could not read config file: {config_path}")
    configured = parser.get("options", "data_dir", fallback="").strip()
    if configured:
        return Path(configured).expanduser()
    base = home_path if home_path is not None else Path.home()
    return base / ".local" / "share" / "Odoo"



def filestore_path(config_path: Path, db_name: str, home_path: Path | None = None) -> Path:
    filestore_root = (resolve_data_dir(config_path, home_path) / "filestore").resolve(strict=False)
    filestore = (filestore_root / validate_db_name(db_name)).resolve(strict=False)
    try:
        filestore.relative_to(filestore_root)
    except ValueError as exc:
        raise ValueError(f"Invalid filestore path for db_name: {db_name!r}") from exc
    return filestore



def cleanup_database(
    *,
    db_name: str,
    config_path: Path,
    dry_run: bool,
    run_command: Callable[..., object] = subprocess.run,
    remove_tree: Callable[[Path], None] = shutil.rmtree,
) -> None:
    db_name = validate_db_name(db_name)
    filestore = filestore_path(config_path, db_name)
    dropdb_cmd = ["dropdb", "--if-exists", db_name]
    print("Cleanup database:", " ".join(dropdb_cmd))
    print("Cleanup filestore:", filestore)

    if dry_run:
        return

    run_command(dropdb_cmd, check=True)
    if filestore.exists():
        remove_tree(filestore)



def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    cleanup_database(db_name=args.db, config_path=Path(args.config).expanduser(), dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
