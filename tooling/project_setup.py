from __future__ import annotations

import argparse
import shlex
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tooling.local_setup_common import (
    build_base_cmd,
    load_json_file,
    merge_settings_local,
    repo_looks_odoo,
    require_existing_path,
    resolve_project_root,
    resolve_version_or_prompt,
    validate_base_cmd,
    write_json_file,
)
from tooling.materialization.materialize_odoo_skill_paths import normalize_series


@dataclass(frozen=True)
class ExistingProjectSetup:
    settings_path: Path
    state_path: Path
    settings_data: dict[str, Any]
    state_data: dict[str, Any]
    base_cmd: str | None
    base_cmd_valid: bool
    state_valid: bool


MANAGED_STATE_KEYS = ("docsRoot", "sourceRoot", "version", "majorVersion")


def _register_parser_arguments(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("--docs-root", help="Absolute path to Odoo documentation repo")
    parser.add_argument("--source-root", help="Absolute path to Odoo source repo")
    parser.add_argument("--version", help="Odoo series like 18.0")
    parser.add_argument("--python-bin", default=None, help="Python executable to run odoo-bin")
    parser.add_argument("--odoo-bin", help="Absolute path to odoo-bin")
    parser.add_argument("--config", help="Absolute path to Odoo config file")
    parser.add_argument("--base-cmd", help="Full ODOO_TEST_BASE_CMD to store directly")
    parser.add_argument("--yes", action="store_true", help="Run non-interactively")
    parser.add_argument("--force", action="store_true", help="Refresh managed values")
    parser.add_argument("--dry-run", action="store_true", help="Print what would change without writing files")
    return parser


def _build_parser(*, prog: str | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        description="Configure project-local Odoo Claude settings",
    )
    return _register_parser_arguments(parser)


def validate_project_setup_args(args: argparse.Namespace, parser: argparse.ArgumentParser) -> argparse.Namespace:
    if args.base_cmd and (args.odoo_bin or args.config):
        parser.error("--base-cmd cannot be combined with --odoo-bin or --config")
    return args


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return validate_project_setup_args(args, parser)


def add_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(
        "project-setup",
        help="Configure project-local Odoo settings",
        description="Configure project-local Odoo Claude settings",
    )
    return _register_parser_arguments(parser)


def _extract_config_path(base_argv: list[str]) -> str | None:
    for index, token in enumerate(base_argv):
        if token == "-c" and index + 1 < len(base_argv):
            return base_argv[index + 1]
        if token.startswith("--config="):
            return token.split("=", 1)[1]
        if token == "--config" and index + 1 < len(base_argv):
            return base_argv[index + 1]
    return None


def _derive_saved_command_parts(base_cmd: str | None) -> tuple[str | None, str | None, str | None]:
    if not base_cmd:
        return None, None, None
    argv = shlex.split(base_cmd)
    python_bin = argv[0] if argv else None
    odoo_bin = argv[1] if len(argv) > 1 else None
    config_path = _extract_config_path(argv)
    return python_bin, odoo_bin, config_path


def _saved_base_cmd_paths_are_usable(base_cmd: str | None) -> bool:
    _, odoo_bin, config_path = _derive_saved_command_parts(base_cmd)
    if not odoo_bin or not config_path:
        return False
    return Path(odoo_bin).is_file() and Path(config_path).is_file()


def load_existing_project_setup(project_root: Path) -> ExistingProjectSetup:
    settings_path = project_root / ".claude" / "settings.local.json"
    state_path = project_root / ".claude" / "odoo-skill-paths.json"
    settings_data = load_json_file(settings_path)
    state_data = load_json_file(state_path)

    env = settings_data.get("env")
    raw_base_cmd = str(env.get("ODOO_TEST_BASE_CMD", "")).strip() if isinstance(env, dict) else ""

    try:
        base_cmd = validate_base_cmd(raw_base_cmd) if raw_base_cmd else None
        base_cmd_valid = bool(base_cmd) and _saved_base_cmd_paths_are_usable(base_cmd)
    except SystemExit:
        base_cmd = None
        base_cmd_valid = False

    state_valid = all(str(state_data.get(key, "")).strip() for key in MANAGED_STATE_KEYS) and all(
        Path(str(state_data.get(path_key, "")).strip()).is_dir()
        for path_key in ("docsRoot", "sourceRoot")
    )

    return ExistingProjectSetup(
        settings_path=settings_path,
        state_path=state_path,
        settings_data=settings_data,
        state_data=state_data,
        base_cmd=base_cmd,
        base_cmd_valid=base_cmd_valid,
        state_valid=state_valid,
    )


def build_state_payload(
    *,
    project_root: Path,
    docs_root: Path,
    source_root: Path,
    version: str,
    version_source: str,
) -> dict[str, str]:
    return {
        "docsRoot": str(docs_root),
        "sourceRoot": str(source_root),
        "version": version,
        "majorVersion": version.split(".", 1)[0],
        "versionSource": version_source,
        "projectRoot": str(project_root.resolve()),
        "configuredAt": datetime.now(timezone.utc).isoformat(),
        "mode": "project-setup",
    }


def _merge_state(existing_state: dict[str, Any], managed_payload: dict[str, str]) -> dict[str, Any]:
    merged = dict(existing_state)
    merged.update(managed_payload)
    return merged


def _print_summary(project_root: Path, version: str, base_cmd_source: str, *, dry_run: bool) -> None:
    prefix = "Dry run" if dry_run else "Configured"
    print(f"{prefix} project setup for {project_root}")
    print(f"Odoo version: {version}")
    print(f"Base command source: {base_cmd_source}")


def run_project_setup(args: argparse.Namespace, *, cwd: Path | None = None) -> int:
    project_root = resolve_project_root(cwd or Path.cwd())
    if not repo_looks_odoo(project_root):
        raise SystemExit(f"Current directory does not look like an Odoo project: {project_root}")

    existing = load_existing_project_setup(project_root)
    if existing.base_cmd_valid and existing.state_valid and not args.force:
        print(f"Project setup already exists for {project_root}")
        print(f"Odoo version: {existing.state_data['version']}")
        print("Base command source: .claude/settings.local.json")
        return 0

    interactive = not args.yes
    saved_docs_root = str(existing.state_data.get("docsRoot", "")).strip() or None
    saved_source_root = str(existing.state_data.get("sourceRoot", "")).strip() or None
    saved_version = str(existing.state_data.get("version", "")).strip() or None
    saved_python_bin, saved_odoo_bin, saved_config_path = _derive_saved_command_parts(existing.base_cmd)

    docs_root = require_existing_path(
        args.docs_root or saved_docs_root,
        "--docs-root",
        "Docs root",
        interactive,
        expected_kind="dir",
    )
    source_root = require_existing_path(
        args.source_root or saved_source_root,
        "--source-root",
        "Source root",
        interactive,
        expected_kind="dir",
    )

    if args.version:
        version = normalize_series(args.version)
        version_source = "--version"
    elif saved_version and not args.force:
        version = normalize_series(saved_version)
        version_source = "saved state"
    else:
        version, version_source = resolve_version_or_prompt(
            saved_version,
            docs_root,
            source_root,
            interactive=interactive,
        )

    if args.base_cmd:
        base_cmd = validate_base_cmd(args.base_cmd)
        base_cmd_source = "--base-cmd"
    elif existing.base_cmd_valid and not args.force and not args.odoo_bin and not args.config:
        base_cmd = existing.base_cmd
        base_cmd_source = ".claude/settings.local.json"
    else:
        python_bin = args.python_bin or saved_python_bin or "python3"
        odoo_bin = require_existing_path(
            args.odoo_bin or saved_odoo_bin,
            "--odoo-bin",
            "odoo-bin path",
            interactive,
            expected_kind="file",
        )
        config_path = require_existing_path(
            args.config or saved_config_path,
            "--config",
            "Odoo config path",
            interactive,
            expected_kind="file",
        )
        base_cmd = validate_base_cmd(build_base_cmd(python_bin, odoo_bin, config_path))
        base_cmd_source = "built from paths"

    state_payload = build_state_payload(
        project_root=project_root,
        docs_root=docs_root,
        source_root=source_root,
        version=version,
        version_source=version_source,
    )
    merged_state = _merge_state(existing.state_data, state_payload)
    merged_settings = merge_settings_local(existing.settings_data, base_cmd)

    if args.dry_run:
        _print_summary(project_root, version, base_cmd_source, dry_run=True)
        print(f"Final ODOO_TEST_BASE_CMD: {base_cmd}")
        print(f"Would write: {existing.settings_path}")
        print(f"Would write: {existing.state_path}")
        return 0

    write_json_file(existing.settings_path, merged_settings)
    write_json_file(existing.state_path, merged_state)
    _print_summary(project_root, version, base_cmd_source, dry_run=False)
    print(f"Wrote: {existing.settings_path}")
    print(f"Wrote: {existing.state_path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    return run_project_setup(parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
