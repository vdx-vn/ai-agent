from __future__ import annotations

import json
import shlex
import subprocess
from copy import deepcopy
from pathlib import Path
from typing import Any

from tooling.materialization.materialize_odoo_skill_paths import normalize_series, resolve_series

ODOO_MARKERS = ["odoo-bin", "addons", "odoo"]
MAX_MANIFEST_SCAN_DEPTH = 2


def load_json_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def write_json_file(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def build_base_cmd(python_bin: str, odoo_bin: str | Path, config_path: str | Path) -> str:
    return f'{shlex.quote(python_bin)} "{odoo_bin}" -c "{config_path}"'


def validate_base_cmd(base_cmd: str) -> str:
    try:
        argv = shlex.split(base_cmd)
    except ValueError as exc:
        raise SystemExit(f"ODOO_TEST_BASE_CMD is not a valid shell command: {exc}") from exc
    if not argv:
        raise SystemExit("ODOO_TEST_BASE_CMD must not be empty")

    has_config = False
    runtime_managed_exact = {
        "-d",
        "--database",
        "--test-tags",
        "-i",
        "--init",
        "-u",
        "--update",
        "--test-enable",
        "--stop-after-init",
    }
    runtime_managed_prefixes = (
        "--database=",
        "--test-tags=",
        "--init=",
        "--update=",
        "-d",
        "-i",
        "-u",
    )

    for index, token in enumerate(argv):
        if token == "-c" and index + 1 < len(argv):
            has_config = True
            continue
        if token == "--config" and index + 1 < len(argv):
            has_config = True
            continue
        if token.startswith("--config="):
            has_config = True
            continue
        if token in runtime_managed_exact:
            raise SystemExit(f"ODOO_TEST_BASE_CMD must not include runtime-managed flag: {token}")
        for prefix in runtime_managed_prefixes:
            if token.startswith(prefix):
                raise SystemExit(f"ODOO_TEST_BASE_CMD must not include runtime-managed flag: {prefix}")

    if not has_config:
        raise SystemExit("ODOO_TEST_BASE_CMD must include -c /path/to/odoo.conf or --config /path/to/odoo.conf")
    return base_cmd


def merge_settings_local(existing: dict[str, Any], base_cmd: str) -> dict[str, Any]:
    merged = deepcopy(existing)
    env = merged.get("env")
    if not isinstance(env, dict):
        env = {}
    else:
        env = dict(env)
    env["ODOO_TEST_BASE_CMD"] = base_cmd
    merged["env"] = env
    return merged


def remove_managed_settings(existing: dict[str, Any], managed_keys: dict[str, list[str]]) -> dict[str, Any]:
    cleaned = deepcopy(existing)
    for top_level_key, nested_keys in managed_keys.items():
        current = cleaned.get(top_level_key)
        if not isinstance(current, dict):
            continue
        updated = dict(current)
        for nested_key in nested_keys:
            updated.pop(nested_key, None)
        if updated:
            cleaned[top_level_key] = updated
        else:
            cleaned.pop(top_level_key, None)
    return cleaned


def prompt_value(label: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    raw = input(f"{label}{suffix}: ").strip()
    return raw or (default or "")


def require_existing_path(
    raw_value: str | None,
    option_name: str,
    prompt_label: str,
    interactive: bool,
    *,
    expected_kind: str | None = None,
) -> Path:
    value = (raw_value or "").strip()
    if not value and interactive:
        value = prompt_value(prompt_label)
    if not value:
        raise SystemExit(f"Missing required value {option_name}")
    raw_path = Path(value).expanduser()
    if not raw_path.is_absolute():
        raise SystemExit(f"Path for {option_name} must be absolute: {value}")
    path = raw_path.resolve()
    if not path.exists():
        raise SystemExit(f"Path does not exist for {option_name}: {path}")
    if expected_kind == "dir" and not path.is_dir():
        raise SystemExit(f"Path for {option_name} must be an existing directory: {path}")
    if expected_kind == "file" and not path.is_file():
        raise SystemExit(f"Path for {option_name} must be an existing file: {path}")
    return path


def resolve_version_or_prompt(
    args_version: str | None,
    docs_root: Path,
    source_root: Path,
    *,
    interactive: bool,
) -> tuple[str, str]:
    try:
        return resolve_series(args_version, docs_root, source_root)
    except SystemExit:
        if not interactive:
            raise
        version_input = prompt_value("Odoo version")
        if not version_input:
            raise SystemExit("Missing required value --version")
        return normalize_series(version_input), "prompt"


def repo_looks_odoo(repo_root: Path) -> bool:
    for marker in ODOO_MARKERS:
        if (repo_root / marker).exists():
            return True

    for manifest in repo_root.rglob("__manifest__.py"):
        try:
            depth = len(manifest.relative_to(repo_root).parts)
        except ValueError:
            continue
        if depth <= MAX_MANIFEST_SCAN_DEPTH:
            return True
    return False


def resolve_project_root(start_dir: Path) -> Path:
    start_dir = start_dir.resolve()
    try:
        result = subprocess.run(
            ["git", "-C", str(start_dir), "rev-parse", "--show-toplevel"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return start_dir

    if result.returncode == 0 and result.stdout.strip():
        return Path(result.stdout.strip()).resolve()
    return start_dir
