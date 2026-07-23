from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tooling.local_setup_common import (
    load_json_file,
    repo_looks_odoo,
    require_existing_path,
    resolve_project_root,
    resolve_version_or_prompt,
    write_json_file,
)
from tooling.materialization.materialize_odoo_skill_paths import normalize_series


@dataclass(frozen=True)
class ExistingProjectSetup:
    state_path: Path
    state_data: dict[str, Any]
    state_valid: bool


MANAGED_STATE_KEYS = ("docsRoot", "sourceRoot", "version", "majorVersion")
SHARED_CONFIG_RELATIVE_PATH = Path(".odoo-skills") / "project.json"
CLAUDE_STATE_RELATIVE_PATH = Path(".claude") / "odoo-skill-paths.json"


def _register_parser_arguments(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("--docs-root", help="Absolute path to Odoo documentation repo")
    parser.add_argument("--source-root", help="Absolute path to Odoo source repo")
    parser.add_argument("--version", help="Odoo series like 18.0")
    parser.add_argument("--yes", action="store_true", help="Run non-interactively")
    parser.add_argument("--force", action="store_true", help="Refresh managed values")
    parser.add_argument("--dry-run", action="store_true", help="Print what would change without writing files")
    return parser


def _build_parser(*, prog: str | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        description="Configure project-local Odoo settings for Codex CLI and Claude Code",
    )
    return _register_parser_arguments(parser)


def validate_project_setup_args(args: argparse.Namespace, parser: argparse.ArgumentParser) -> argparse.Namespace:
    return args


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return validate_project_setup_args(args, parser)


def add_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(
        "project-setup",
        help="Configure project-local Odoo settings",
        description="Configure project-local Odoo settings for Codex CLI and Claude Code",
    )
    return _register_parser_arguments(parser)


def load_existing_project_setup(project_root: Path) -> ExistingProjectSetup:
    state_path = project_root / CLAUDE_STATE_RELATIVE_PATH
    shared_path = project_root / SHARED_CONFIG_RELATIVE_PATH
    legacy_state_data = load_json_file(state_path)
    shared_data = load_json_file(shared_path)
    state_data = shared_data or legacy_state_data

    state_valid = all(str(state_data.get(key, "")).strip() for key in MANAGED_STATE_KEYS) and all(
        Path(str(state_data.get(path_key, "")).strip()).is_dir()
        for path_key in ("docsRoot", "sourceRoot")
    )

    return ExistingProjectSetup(
        state_path=state_path,
        state_data=state_data,
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


def _print_summary(project_root: Path, version: str, *, dry_run: bool) -> None:
    prefix = "Dry run" if dry_run else "Configured"
    print(f"{prefix} project setup for {project_root}")
    print(f"Odoo version: {version}")


def _find_extra_addons_candidate(project_root: Path, start_dir: Path) -> Path | None:
    for base in (start_dir, project_root):
        candidate = base / "extra-addons"
        if candidate.is_dir():
            return candidate
    for candidate in project_root.rglob("extra-addons"):
        if candidate.is_dir():
            return candidate
    return None


def run_project_setup(args: argparse.Namespace, *, cwd: Path | None = None) -> int:
    start_dir = (cwd or Path.cwd()).resolve()
    project_root = resolve_project_root(start_dir)
    if not repo_looks_odoo(project_root) and not repo_looks_odoo(start_dir):
        extra = _find_extra_addons_candidate(project_root, start_dir)
        if extra is None or not repo_looks_odoo(extra):
            raise SystemExit(f"Current directory does not look like an Odoo project: {project_root}")

    existing = load_existing_project_setup(project_root)
    shared_path = project_root / SHARED_CONFIG_RELATIVE_PATH
    if (
        existing.state_valid
        and shared_path.exists()
        and existing.state_path.exists()
        and not args.force
    ):
        print(f"Project setup already exists for {project_root}")
        print(f"Odoo version: {existing.state_data['version']}")
        return 0

    interactive = not args.yes
    saved_docs_root = str(existing.state_data.get("docsRoot", "")).strip() or None
    saved_source_root = str(existing.state_data.get("sourceRoot", "")).strip() or None
    saved_version = str(existing.state_data.get("version", "")).strip() or None

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

    state_payload = build_state_payload(
        project_root=project_root,
        docs_root=docs_root,
        source_root=source_root,
        version=version,
        version_source=version_source,
    )
    merged_state = _merge_state(existing.state_data, state_payload)
    merged_state["schemaVersion"] = "1"

    if args.dry_run:
        _print_summary(project_root, version, dry_run=True)
        print(f"Would write: {shared_path}")
        print(f"Would write: {existing.state_path}")
        return 0

    write_json_file(shared_path, merged_state)
    write_json_file(existing.state_path, merged_state)
    _print_summary(project_root, version, dry_run=False)
    print(f"Wrote: {shared_path}")
    print(f"Wrote: {existing.state_path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    return run_project_setup(parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
