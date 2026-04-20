#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tooling.build_plugin import build_marketplace
from tooling.local_setup_common import (
    build_base_cmd,
    load_json_file,
    merge_settings_local,
    remove_managed_settings,
    require_existing_path as _require_existing_path,
    resolve_version_or_prompt as _resolve_version_or_prompt,
    validate_base_cmd,
    write_json_file,
)
from tooling.materialization.materialize_odoo_skill_paths import materialize_skills


@dataclass(frozen=True)
class SetupInputs:
    docs_root: Path
    source_root: Path
    version: str
    python_bin: str
    odoo_bin: Path | None
    config_path: Path | None
    base_cmd: str
    yes: bool
    uninstall: bool


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect local Odoo setup inputs")
    parser.add_argument("--docs-root", help="Absolute path to Odoo documentation repo")
    parser.add_argument("--source-root", help="Absolute path to Odoo source repo")
    parser.add_argument("--version", help="Odoo series like 18.0")
    parser.add_argument("--python-bin", default="python3", help="Python executable to run odoo-bin")
    parser.add_argument("--odoo-bin", help="Absolute path to odoo-bin")
    parser.add_argument("--config", help="Absolute path to Odoo config file")
    parser.add_argument("--base-cmd", help="Full ODOO_TEST_BASE_CMD to store directly")
    parser.add_argument("--yes", action="store_true", help="Run non-interactively")
    parser.add_argument("--uninstall", action="store_true", help="Remove managed local setup")
    return parser.parse_args(argv)


def _resolve_version(args: argparse.Namespace, docs_root: Path, source_root: Path) -> str:
    version, _source = _resolve_version_or_prompt(
        args.version,
        docs_root,
        source_root,
        interactive=not args.yes,
    )
    return version


def collect_setup_inputs(repo_root: Path, args: argparse.Namespace) -> SetupInputs:
    del repo_root
    interactive = not args.yes
    docs_root = _require_existing_path(
        args.docs_root,
        "--docs-root",
        "Docs root",
        interactive,
        expected_kind="dir",
    )
    source_root = _require_existing_path(
        args.source_root,
        "--source-root",
        "Source root",
        interactive,
        expected_kind="dir",
    )
    version = _resolve_version(args, docs_root, source_root)

    if args.base_cmd:
        return SetupInputs(
            docs_root=docs_root,
            source_root=source_root,
            version=version,
            python_bin=args.python_bin,
            odoo_bin=None,
            config_path=None,
            base_cmd=validate_base_cmd(args.base_cmd),
            yes=args.yes,
            uninstall=args.uninstall,
        )

    odoo_bin = _require_existing_path(
        args.odoo_bin,
        "--odoo-bin",
        "odoo-bin path",
        interactive,
        expected_kind="file",
    )
    config_path = _require_existing_path(
        args.config,
        "--config",
        "Odoo config path",
        interactive,
        expected_kind="file",
    )
    base_cmd = build_base_cmd(args.python_bin, odoo_bin, config_path)
    return SetupInputs(
        docs_root=docs_root,
        source_root=source_root,
        version=version,
        python_bin=args.python_bin,
        odoo_bin=odoo_bin,
        config_path=config_path,
        base_cmd=base_cmd,
        yes=args.yes,
        uninstall=args.uninstall,
    )


def ensure_claude_cli(*, required: bool = True) -> bool:
    if shutil.which("claude"):
        return True
    if required:
        raise SystemExit("Claude CLI is required. Install `claude` and try again.")
    return False


def run_command(repo_root: Path, command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=repo_root, check=True, capture_output=True, text=True)


def update_setup_state(config_path: Path, **fields: Any) -> dict[str, Any]:
    state = load_json_file(config_path)
    state.update(fields)
    write_json_file(config_path, state)
    return state


def _error_text(exc: BaseException) -> str:
    stderr = getattr(exc, "stderr", None)
    stdout = getattr(exc, "stdout", None)
    parts = [part.decode(errors="replace") if isinstance(part, bytes) else str(part) for part in (stderr, stdout) if part]
    parts.append(str(exc))
    return "\n".join(parts).lower()


def add_marketplace(repo_root: Path, marketplace_path: Path) -> None:
    add_command = ["claude", "plugin", "marketplace", "add", str(marketplace_path)]
    try:
        run_command(repo_root, add_command)
    except subprocess.CalledProcessError as exc:
        if "exist" not in _error_text(exc):
            raise
        run_command(repo_root, ["claude", "plugin", "marketplace", "remove", "odoo-skills-dev"])
        run_command(repo_root, add_command)


def restore_materialized_files(
    repo_root: Path,
    relative_paths: list[str],
    backups: dict[str, str] | None = None,
) -> None:
    backup_map = backups or {}
    for relative_path in relative_paths:
        target_path = Path(relative_path)
        if not target_path.is_absolute():
            target_path = repo_root / target_path
        backup_text = backup_map.get(str(target_path))
        if backup_text is None:
            continue
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(backup_text, encoding="utf-8")


def _capture_materialized_backups(skills_root: Path) -> dict[str, str]:
    backups: dict[str, str] = {}
    if not skills_root.exists():
        return backups
    for path in skills_root.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".yaml", ".yml"}:
            backups[str(path.resolve())] = path.read_text(encoding="utf-8")
    return backups


def _best_effort_run_command(repo_root: Path, command: list[str]) -> None:
    try:
        run_command(repo_root, command)
    except Exception:
        pass


def run_setup(repo_root: Path, args: argparse.Namespace) -> int:
    ensure_claude_cli()
    inputs = collect_setup_inputs(repo_root, args)
    settings_path = repo_root / ".claude" / "settings.local.json"
    state_path = repo_root / ".claude" / "odoo-skill-paths.json"
    marketplace_path = repo_root / "dist" / "marketplace"
    skills_root = repo_root / ".claude" / "skills"
    managed_settings = {"env": ["ODOO_TEST_BASE_CMD"]}
    had_settings = settings_path.exists()
    original_settings = settings_path.read_text(encoding="utf-8") if had_settings else None
    original_materialized_backups = _capture_materialized_backups(skills_root)

    materialized_files: list[str] = []
    materialized_backups: dict[str, str] = {}
    marketplace_added = False
    plugin_installed = False

    try:
        merged_settings = merge_settings_local(load_json_file(settings_path), inputs.base_cmd)
        write_json_file(settings_path, merged_settings)

        setup_metadata = {
            "managedSettings": managed_settings,
            "pluginName": "odoo-skills",
            "marketplaceName": "odoo-skills-dev",
            "installScope": "local",
            "marketplacePath": str(marketplace_path),
        }
        materialization_result = materialize_skills(
            docs_root=inputs.docs_root,
            source_root=inputs.source_root,
            skills_root=skills_root,
            config_path=state_path,
            version=inputs.version,
            extra_metadata=setup_metadata,
        )
        materialized_files = [str(path) for path in materialization_result.materialized_files]
        materialized_backups = {
            path: original_materialized_backups[path]
            for path in materialized_files
            if path in original_materialized_backups
        }
        if materialized_backups:
            setup_metadata["materializedBackups"] = materialized_backups
            update_setup_state(state_path, materializedBackups=materialized_backups)
        built_marketplace = build_marketplace(repo_root, marketplace_path)
        update_setup_state(state_path, **setup_metadata)
        run_command(repo_root, ["claude", "plugin", "validate", str(built_marketplace)])
        add_marketplace(repo_root, built_marketplace)
        marketplace_added = True
        run_command(repo_root, ["claude", "plugin", "install", "odoo-skills@odoo-skills-dev", "--scope", "local"])
        plugin_installed = True
        update_setup_state(state_path, setupCompletedAt=datetime.now(timezone.utc).isoformat())
    except Exception:
        if plugin_installed:
            _best_effort_run_command(repo_root, ["claude", "plugin", "uninstall", "odoo-skills", "--scope", "local"])
        if marketplace_added:
            _best_effort_run_command(repo_root, ["claude", "plugin", "marketplace", "remove", "odoo-skills-dev"])
        if materialized_files:
            restore_materialized_files(repo_root, materialized_files, materialized_backups)
        if marketplace_path.exists():
            shutil.rmtree(marketplace_path)
        if had_settings and original_settings is not None:
            settings_path.parent.mkdir(parents=True, exist_ok=True)
            settings_path.write_text(original_settings, encoding="utf-8")
        elif settings_path.exists():
            settings_path.unlink()
        if state_path.exists():
            state_path.unlink()
        raise

    print(f"Setup complete for {repo_root}")
    print(f"To uninstall: python3 {Path(__file__).resolve()} --uninstall")
    return 0


def run_uninstall(repo_root: Path, args: argparse.Namespace) -> int:
    del args
    state_path = repo_root / ".claude" / "odoo-skill-paths.json"
    settings_path = repo_root / ".claude" / "settings.local.json"
    dist_marketplace = repo_root / "dist" / "marketplace"
    state = load_json_file(state_path)

    if state and ensure_claude_cli(required=False):
        plugin_name = state.get("pluginName")
        install_scope = state.get("installScope")
        if plugin_name and install_scope:
            _best_effort_run_command(repo_root, ["claude", "plugin", "uninstall", plugin_name, "--scope", install_scope])
        marketplace_name = state.get("marketplaceName")
        if marketplace_name:
            _best_effort_run_command(repo_root, ["claude", "plugin", "marketplace", "remove", marketplace_name])

    materialized_files = state.get("materializedFiles")
    materialized_backups = state.get("materializedBackups")
    if isinstance(materialized_files, list) and materialized_files:
        restore_materialized_files(
            repo_root,
            materialized_files,
            materialized_backups if isinstance(materialized_backups, dict) else {},
        )

    managed_settings = state.get("managedSettings")
    if not isinstance(managed_settings, dict):
        managed_settings = {"env": ["ODOO_TEST_BASE_CMD"]}
    if settings_path.exists():
        cleaned_settings = remove_managed_settings(load_json_file(settings_path), managed_settings)
        if cleaned_settings:
            write_json_file(settings_path, cleaned_settings)
        else:
            settings_path.unlink()

    if dist_marketplace.exists():
        shutil.rmtree(dist_marketplace)
    if state_path.exists():
        state_path.unlink()
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(__file__).resolve().parents[1]
    if args.uninstall:
        return run_uninstall(repo_root, args)
    return run_setup(repo_root, args)


if __name__ == "__main__":
    raise SystemExit(main())
