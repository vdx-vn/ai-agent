#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

PATH_PLACEHOLDERS = {
    "<ODOO_DOCS_ROOT>": "docsRoot",
    "<ODOO_SOURCE_ROOT>": "sourceRoot",
}
VERSION_PLACEHOLDERS = {
    "<ODOO_SERIES>": "version",
    "<ODOO_MAJOR_VERSION>": "majorVersion",
}
TEXT_SUFFIXES = {".md", ".yaml", ".yml"}
SERIES_RE = re.compile(r"(?<!\d)(\d{2})[._-]0(?!\d)")
MAJOR_RE = re.compile(r"(?<!\d)(\d{2})(?!\d)")


@dataclass(frozen=True)
class MaterializationResult:
    version: str
    major_version: str
    version_source: str
    mode: str
    materialized_files: list[Path]


def parse_args() -> argparse.Namespace:
    script_path = Path(__file__).resolve()
    default_skills_root = script_path.parents[1]
    default_project_root = script_path.parents[3]

    parser = argparse.ArgumentParser(
        description="Materialize Odoo skill placeholders into real paths and a concrete Odoo version for one project copy."
    )
    parser.add_argument("--docs-root", required=True, help="Absolute path to Odoo documentation repo")
    parser.add_argument("--source-root", required=True, help="Absolute path to Odoo source repo")
    parser.add_argument(
        "--version",
        help="Odoo series like 17.0, 18.0, or 19.0. If omitted, the script will try to detect it from git branches or path names.",
    )
    parser.add_argument(
        "--skills-root",
        default=str(default_skills_root),
        help="Path to the copied .claude/skills directory to materialize",
    )
    parser.add_argument(
        "--config-path",
        default=str(default_project_root / ".claude" / "odoo-skill-paths.json"),
        help="Where to write resolved path and version metadata",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print files that would change without writing")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-materialize an already customized copy using values from the existing config file",
    )
    return parser.parse_args()


def normalize_series(raw: str) -> str:
    value = raw.strip()
    if re.fullmatch(r"\d{2}", value):
        return f"{value}.0"
    if re.fullmatch(r"\d{2}\.0", value):
        return value
    raise SystemExit(f"Unsupported Odoo version format: {raw}. Use values like 17.0, 18.0, or 19.0")


def major_from_series(series: str) -> str:
    return series.split(".", 1)[0]


def detect_series_from_git(repo_root: Path) -> tuple[str | None, str | None]:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "branch", "--show-current"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None, None

    branch = result.stdout.strip()
    if not branch:
        return None, None
    match = SERIES_RE.search(branch)
    if match:
        return f"{match.group(1)}.0", f"git branch {branch}"
    return None, None


def detect_series_from_path(path: Path) -> tuple[str | None, str | None]:
    for candidate in [path, *path.parents[:2]]:
        name = candidate.name
        series_match = SERIES_RE.search(name)
        if series_match:
            return f"{series_match.group(1)}.0", f"path name {name}"
        major_match = MAJOR_RE.search(name)
        if major_match:
            return f"{major_match.group(1)}.0", f"path name {name}"
    return None, None


def resolve_series(args_version: str | None, docs_root: Path, source_root: Path) -> tuple[str, str]:
    if args_version:
        series = normalize_series(args_version)
        return series, "--version"

    for root in (source_root, docs_root):
        series, source = detect_series_from_git(root)
        if series:
            return series, source

    for root in (source_root, docs_root):
        series, source = detect_series_from_path(root)
        if series:
            return series, source

    raise SystemExit(
        "Could not detect Odoo version from git branches or path names. Pass --version 18.0 (or another supported series)."
    )


def resolve_existing_config(config_path: Path) -> dict[str, str]:
    if not config_path.exists():
        return {}
    data = json.loads(config_path.read_text(encoding="utf-8"))
    return {
        "docsRoot": data.get("docsRoot", ""),
        "sourceRoot": data.get("sourceRoot", ""),
        "version": data.get("version", ""),
        "majorVersion": data.get("majorVersion", ""),
    }


def iter_text_files(skills_root: Path) -> Iterable[Path]:
    for path in skills_root.rglob("*"):
        if path.is_file() and path.suffix in TEXT_SUFFIXES:
            yield path


def replace_placeholders(text: str, docs_root: str, source_root: str, version: str, major: str) -> tuple[str, bool]:
    updated = text
    replacements = {
        "<ODOO_DOCS_ROOT>": docs_root,
        "<ODOO_SOURCE_ROOT>": source_root,
        "<ODOO_SERIES>": version,
        "<ODOO_MAJOR_VERSION>": major,
    }
    changed = False
    for old, new in replacements.items():
        if old in updated:
            updated = updated.replace(old, new)
            changed = True
    return updated, changed


def replace_existing_materialized(
    text: str,
    existing: dict[str, str],
    docs_root: str,
    source_root: str,
    version: str,
    major: str,
) -> tuple[str, bool]:
    updated = text
    changed = False

    exact_replacements = {
        existing.get("docsRoot", ""): docs_root,
        existing.get("sourceRoot", ""): source_root,
    }
    for old, new in exact_replacements.items():
        if old and old in updated:
            updated = updated.replace(old, new)
            changed = True

    old_series = existing.get("version", "")
    old_major = existing.get("majorVersion", "")
    phrase_replacements = {
        f"Odoo CE {old_major}": f"Odoo CE {major}",
        f"Odoo {old_major}": f"Odoo {major}",
        f"branch {old_series}": f"branch {version}",
        f"Series: {old_series}": f"Series: {version}",
        f"Major: {old_major}": f"Major: {major}",
    }
    for old, new in phrase_replacements.items():
        if old and old in updated:
            updated = updated.replace(old, new)
            changed = True

    return updated, changed


def validate_inputs(docs_root: Path, source_root: Path, skills_root: Path) -> None:
    if not docs_root.exists() or not docs_root.is_dir():
        raise SystemExit(f"Docs root not found or not a directory: {docs_root}")
    if not source_root.exists() or not source_root.is_dir():
        raise SystemExit(f"Source root not found or not a directory: {source_root}")
    if not skills_root.exists() or not skills_root.is_dir():
        raise SystemExit(f"Skills root not found or not a directory: {skills_root}")


def materialize_skills(
    *,
    docs_root: Path,
    source_root: Path,
    skills_root: Path,
    config_path: Path,
    version: str | None = None,
    dry_run: bool = False,
    force: bool = False,
    extra_metadata: dict[str, object] | None = None,
) -> MaterializationResult:
    docs_root = docs_root.expanduser().resolve()
    source_root = source_root.expanduser().resolve()
    skills_root = skills_root.expanduser().resolve()
    config_path = config_path.expanduser().resolve()
    validate_inputs(docs_root, source_root, skills_root)

    series, version_source = resolve_series(version, docs_root, source_root)
    major = major_from_series(series)
    existing = resolve_existing_config(config_path)

    changed_files: list[Path] = []
    updated_content: dict[Path, str] = {}
    saw_placeholder = False
    saw_force_update = False

    for path in iter_text_files(skills_root):
        text = path.read_text(encoding="utf-8")
        if any(token in text for token in [*PATH_PLACEHOLDERS, *VERSION_PLACEHOLDERS]):
            saw_placeholder = True
            new_text, changed = replace_placeholders(text, str(docs_root), str(source_root), series, major)
        elif force and existing:
            new_text, changed = replace_existing_materialized(
                text,
                existing,
                str(docs_root),
                str(source_root),
                series,
                major,
            )
            if changed:
                saw_force_update = True
        else:
            new_text, changed = text, False

        if changed:
            changed_files.append(path)
            updated_content[path] = new_text

    if not changed_files:
        if saw_placeholder:
            raise SystemExit("No writable placeholder replacements were found.")
        if config_path.exists() and not force:
            raise SystemExit(
                "This skill copy already looks materialized. Re-run with --force to replace previously written paths and version phrases."
            )
        raise SystemExit("No placeholder values found. Nothing to materialize.")

    mode = "dry-run" if dry_run else "force" if saw_force_update else "initial"
    result = MaterializationResult(
        version=series,
        major_version=major,
        version_source=version_source,
        mode=mode,
        materialized_files=changed_files,
    )

    if dry_run:
        return result

    for path, content in updated_content.items():
        path.write_text(content, encoding="utf-8")

    config_path.parent.mkdir(parents=True, exist_ok=True)
    config = {
        "docsRoot": str(docs_root),
        "sourceRoot": str(source_root),
        "version": series,
        "majorVersion": major,
        "versionSource": version_source,
        "skillsRoot": str(skills_root),
        "materializedAt": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "materializedFiles": [str(path) for path in changed_files],
    }
    if extra_metadata:
        config.update(extra_metadata)
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> int:
    args = parse_args()
    result = materialize_skills(
        docs_root=Path(args.docs_root),
        source_root=Path(args.source_root),
        version=args.version,
        skills_root=Path(args.skills_root),
        config_path=Path(args.config_path),
        dry_run=args.dry_run,
        force=args.force,
    )

    if args.dry_run:
        for path in result.materialized_files:
            print(path)
        print(f"Detected Odoo version {result.version} from {result.version_source}")
        return 0

    print(f"Materialized {len(result.materialized_files)} files in {Path(args.skills_root).expanduser().resolve()}")
    print(f"Using Odoo version {result.version} ({result.version_source})")
    print(f"Wrote config to {Path(args.config_path).expanduser().resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
