# One-Command Local Setup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a single `python3 tooling/setup_local.py` entrypoint that materializes local Odoo paths, writes `ODOO_TEST_BASE_CMD`, installs the plugin locally, and fully uninstalls the local setup.

**Architecture:** Keep orchestration in a new direct-entry script at `tooling/setup_local.py`, and reuse existing build and materialization utilities rather than duplicating them. Extend the materialization utility with a reusable API and richer state recording so setup and uninstall stay idempotent and only touch setup-managed local state.

**Tech Stack:** Python 3.12, `unittest`, existing `tooling.build_plugin`, existing materialization scripts, Claude CLI plugin commands, JSON local config files

---

## File Map

- Create: `tooling/setup_local.py` — one-command local setup and uninstall orchestration.
- Create: `tests/unit/test_setup_local.py` — parser, prompt, settings merge, command-order, and uninstall cleanup tests with mocked subprocess calls.
- Create: `tests/unit/test_materialize_odoo_skill_paths.py` — reusable materialization helper and metadata coverage.
- Modify: `tooling/materialization/materialize_odoo_skill_paths.py:1-276` — expose reusable helper, preserve CLI behavior, and record richer setup state.
- Modify: `.claude/skills/scripts/materialize_odoo_skill_paths.py:1-276` — keep project-copy manual fallback in sync with the tooling version.
- Modify: `README.md:1-26` — shorten onboarding to one command, document non-interactive flags and uninstall.
- Modify: `tooling/materialization/suggest_odoo_skill_setup.py:1-138` — point hook guidance to `tooling/setup_local.py` first.
- Modify: `.claude/skills/odoo-paths.md:1-48` — document one-command setup and manual fallback.
- Modify: `.claude/skills/scripts/suggest_odoo_skill_setup.py:1-138` — keep copied guidance aligned with tooling version.
- Modify: `tests/unit/test_plugin_foundation.py:1-47` — assert README reflects one-command onboarding.
- Modify: `tests/unit/test_suggest_odoo_skill_setup.py:1-68` — assert hook guidance points to the new entrypoint.

### Task 1: Expose reusable materialization API and richer state

**Files:**
- Create: `tests/unit/test_materialize_odoo_skill_paths.py`
- Modify: `tooling/materialization/materialize_odoo_skill_paths.py:1-276`
- Modify: `.claude/skills/scripts/materialize_odoo_skill_paths.py:1-276`

- [ ] **Step 1: Write the failing materialization tests**

```python
import json
import tempfile
import unittest
from pathlib import Path

from tooling.materialization.materialize_odoo_skill_paths import materialize_skills


class MaterializeOdooSkillPathsTests(unittest.TestCase):
    def test_materialize_skills_replaces_placeholders_and_records_setup_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            docs_root = repo_root / "docs-18.0"
            source_root = repo_root / "odoo-18.0"
            skills_root = repo_root / ".claude" / "skills"
            config_path = repo_root / ".claude" / "odoo-skill-paths.json"
            docs_root.mkdir(parents=True)
            source_root.mkdir(parents=True)
            skills_root.mkdir(parents=True)
            target = skills_root / "odoo-build" / "references" / "overview.md"
            target.parent.mkdir(parents=True)
            target.write_text(
                "Docs: <ODOO_DOCS_ROOT>\n"
                "Src: <ODOO_SOURCE_ROOT>\n"
                "Series: <ODOO_SERIES>\n"
                "Major: <ODOO_MAJOR_VERSION>\n",
                encoding="utf-8",
            )

            result = materialize_skills(
                docs_root=docs_root,
                source_root=source_root,
                skills_root=skills_root,
                config_path=config_path,
                version="18.0",
                force=False,
                extra_metadata={"pluginName": "odoo-skills"},
            )

            self.assertEqual(result.version, "18.0")
            self.assertEqual(result.major_version, "18")
            self.assertEqual(result.changed_files, [target])
            self.assertIn(str(docs_root), target.read_text(encoding="utf-8"))
            config = json.loads(config_path.read_text(encoding="utf-8"))
            self.assertEqual(config["pluginName"], "odoo-skills")
            self.assertEqual(
                config["materializedFiles"],
                [".claude/skills/odoo-build/references/overview.md"],
            )

    def test_materialize_skills_force_rewrites_existing_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            old_docs = repo_root / "docs-17.0"
            old_source = repo_root / "odoo-17.0"
            new_docs = repo_root / "docs-18.0"
            new_source = repo_root / "odoo-18.0"
            skills_root = repo_root / ".claude" / "skills"
            config_path = repo_root / ".claude" / "odoo-skill-paths.json"
            for path in (old_docs, old_source, new_docs, new_source, skills_root):
                path.mkdir(parents=True)
            target = skills_root / "odoo-paths.md"
            target.write_text(
                f"Docs: {old_docs}\n"
                f"Source: {old_source}\n"
                "Odoo 17\n"
                "branch 17.0\n",
                encoding="utf-8",
            )
            config_path.parent.mkdir(parents=True)
            config_path.write_text(
                json.dumps(
                    {
                        "docsRoot": str(old_docs),
                        "sourceRoot": str(old_source),
                        "version": "17.0",
                        "majorVersion": "17",
                    }
                ),
                encoding="utf-8",
            )

            result = materialize_skills(
                docs_root=new_docs,
                source_root=new_source,
                skills_root=skills_root,
                config_path=config_path,
                version="18.0",
                force=True,
            )

            self.assertEqual(result.version_source, "--version")
            text = target.read_text(encoding="utf-8")
            self.assertIn(str(new_docs), text)
            self.assertIn(str(new_source), text)
            self.assertIn("Odoo 18", text)
            self.assertIn("branch 18.0", text)

    def test_materialize_skills_dry_run_reports_changes_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            docs_root = repo_root / "docs-18.0"
            source_root = repo_root / "odoo-18.0"
            skills_root = repo_root / ".claude" / "skills"
            config_path = repo_root / ".claude" / "odoo-skill-paths.json"
            docs_root.mkdir(parents=True)
            source_root.mkdir(parents=True)
            skills_root.mkdir(parents=True)
            target = skills_root / "odoo-paths.md"
            target.write_text("Docs: <ODOO_DOCS_ROOT>\n", encoding="utf-8")

            result = materialize_skills(
                docs_root=docs_root,
                source_root=source_root,
                skills_root=skills_root,
                config_path=config_path,
                version="18.0",
                force=False,
                dry_run=True,
            )

            self.assertEqual(result.changed_files, [target])
            self.assertEqual(target.read_text(encoding="utf-8"), "Docs: <ODOO_DOCS_ROOT>\n")
            self.assertFalse(config_path.exists())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the new tests to confirm the helper is missing**

Run: `python3 -m unittest tests.unit.test_materialize_odoo_skill_paths -v`
Expected: FAIL with `ImportError: cannot import name 'materialize_skills'`

- [ ] **Step 3: Add a reusable `materialize_skills()` helper in the tooling script**

```python
from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class MaterializationResult:
    changed_files: list[Path]
    version: str
    major_version: str
    version_source: str
    config_path: Path


def materialize_skills(
    *,
    docs_root: Path,
    source_root: Path,
    skills_root: Path,
    config_path: Path,
    version: str | None,
    force: bool,
    dry_run: bool = False,
    extra_metadata: dict[str, Any] | None = None,
) -> MaterializationResult:
    if not docs_root.exists() or not docs_root.is_dir():
        raise SystemExit(f"Docs root not found or not a directory: {docs_root}")
    if not source_root.exists() or not source_root.is_dir():
        raise SystemExit(f"Source root not found or not a directory: {source_root}")
    if not skills_root.exists() or not skills_root.is_dir():
        raise SystemExit(f"Skills root not found or not a directory: {skills_root}")

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

    if dry_run:
        return MaterializationResult(
            changed_files=changed_files,
            version=series,
            major_version=major,
            version_source=version_source,
            config_path=config_path,
        )

    for path, content in updated_content.items():
        path.write_text(content, encoding="utf-8")

    repo_root = config_path.parents[1]
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config: dict[str, Any] = {
        "docsRoot": str(docs_root),
        "sourceRoot": str(source_root),
        "version": series,
        "majorVersion": major,
        "versionSource": version_source,
        "skillsRoot": str(skills_root),
        "materializedAt": datetime.now(timezone.utc).isoformat(),
        "mode": "force" if saw_force_update else "initial",
        "materializedFiles": [str(path.relative_to(repo_root)) for path in changed_files],
    }
    if extra_metadata:
        config.update(extra_metadata)
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")

    return MaterializationResult(
        changed_files=changed_files,
        version=series,
        major_version=major,
        version_source=version_source,
        config_path=config_path,
    )
```

Replace the body of `main()` in `tooling/materialization/materialize_odoo_skill_paths.py` with:

```python
def main() -> int:
    args = parse_args()
    result = materialize_skills(
        docs_root=Path(args.docs_root).expanduser().resolve(),
        source_root=Path(args.source_root).expanduser().resolve(),
        skills_root=Path(args.skills_root).expanduser().resolve(),
        config_path=Path(args.config_path).expanduser().resolve(),
        version=args.version,
        force=args.force,
        dry_run=args.dry_run,
    )

    if args.dry_run:
        for path in result.changed_files:
            print(path)
        print(f"Detected Odoo version {result.version} from {result.version_source}")
        return 0

    print(f"Materialized {len(result.changed_files)} files in {Path(args.skills_root).expanduser().resolve()}")
    print(f"Using Odoo version {result.version} ({result.version_source})")
    print(f"Wrote config to {Path(args.config_path).expanduser().resolve()}")
    return 0
```

- [ ] **Step 4: Mirror the same helper and `main()` changes into the copied fallback script**

Apply the same `MaterializationResult`, `materialize_skills()`, and `main()` changes to `.claude/skills/scripts/materialize_odoo_skill_paths.py` so the manual fallback path writes the same config shape and supports the same force-rematerialization behavior.

- [ ] **Step 5: Run the materialization tests again**

Run: `python3 -m unittest tests.unit.test_materialize_odoo_skill_paths -v`
Expected: PASS with `test_materialize_skills_force_rewrites_existing_values ... ok` and `test_materialize_skills_replaces_placeholders_and_records_setup_metadata ... ok`

- [ ] **Step 6: Commit the reusable materialization helper**

```bash
git add tests/unit/test_materialize_odoo_skill_paths.py tooling/materialization/materialize_odoo_skill_paths.py .claude/skills/scripts/materialize_odoo_skill_paths.py
git commit -m "test: cover materialization setup metadata"
```

### Task 2: Add setup-local parser, prompting, and settings merge helpers

**Files:**
- Create: `tooling/setup_local.py`
- Create: `tests/unit/test_setup_local.py`

- [ ] **Step 1: Write failing helper tests for the new setup entrypoint**

```python
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tooling import setup_local


class SetupLocalHelpersTests(unittest.TestCase):
    def test_parse_args_accepts_direct_entrypoint_flags(self) -> None:
        args = setup_local.parse_args(
            [
                "--docs-root",
                "/tmp/docs",
                "--source-root",
                "/tmp/src",
                "--python-bin",
                "python3",
                "--odoo-bin",
                "/tmp/src/odoo-bin",
                "--config",
                "/tmp/odoo.conf",
                "--version",
                "18.0",
                "--yes",
            ]
        )

        self.assertEqual(args.docs_root, "/tmp/docs")
        self.assertEqual(args.source_root, "/tmp/src")
        self.assertEqual(args.python_bin, "python3")
        self.assertTrue(args.yes)
        self.assertFalse(args.uninstall)

    def test_build_base_cmd_uses_python_bin_and_config(self) -> None:
        self.assertEqual(
            setup_local.build_base_cmd("python3", "/srv/odoo/odoo-bin", "/etc/odoo.conf"),
            "python3 /srv/odoo/odoo-bin -c /etc/odoo.conf",
        )

    def test_merge_settings_local_updates_only_odoo_test_base_cmd(self) -> None:
        updated = setup_local.merge_settings_local(
            {
                "env": {"KEEP_ME": "1", "ODOO_TEST_BASE_CMD": "old"},
                "permissions": {"allow": ["Bash(ls)"]},
            },
            "python3 /srv/odoo/odoo-bin -c /etc/odoo.conf",
        )

        self.assertEqual(updated["env"]["KEEP_ME"], "1")
        self.assertEqual(
            updated["env"]["ODOO_TEST_BASE_CMD"],
            "python3 /srv/odoo/odoo-bin -c /etc/odoo.conf",
        )
        self.assertEqual(updated["permissions"], {"allow": ["Bash(ls)"]})

    def test_collect_setup_inputs_prompts_for_missing_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            docs_root = repo_root / "docs-18.0"
            source_root = repo_root / "odoo-18.0"
            odoo_bin = source_root / "odoo-bin"
            config_path = repo_root / "odoo.conf"
            docs_root.mkdir(parents=True)
            source_root.mkdir(parents=True)
            odoo_bin.write_text("", encoding="utf-8")
            config_path.write_text("[options]\n", encoding="utf-8")

            args = setup_local.parse_args([])
            with patch(
                "builtins.input",
                side_effect=[
                    str(docs_root),
                    str(source_root),
                    "18.0",
                    str(odoo_bin),
                    str(config_path),
                ],
            ):
                inputs = setup_local.collect_setup_inputs(repo_root, args)

            self.assertEqual(inputs.docs_root, docs_root)
            self.assertEqual(inputs.source_root, source_root)
            self.assertEqual(inputs.version, "18.0")
            self.assertEqual(inputs.base_cmd, f"python3 {odoo_bin} -c {config_path}")

    def test_collect_setup_inputs_requires_flags_in_non_interactive_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            args = setup_local.parse_args(["--yes"])

            with self.assertRaises(SystemExit) as ctx:
                setup_local.collect_setup_inputs(repo_root, args)

            self.assertIn("Odoo documentation root is required in non-interactive mode", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the helper tests before the script exists**

Run: `python3 -m unittest tests.unit.test_setup_local.SetupLocalHelpersTests -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'tooling.setup_local'`

- [ ] **Step 3: Implement `tooling/setup_local.py` helper layer**

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tooling.materialization.materialize_odoo_skill_paths import resolve_series

PLUGIN_NAME = "odoo-skills"
MARKETPLACE_NAME = "odoo-skills-dev"
INSTALL_SCOPE = "local"
MANAGED_SETTINGS_KEYS = ["env.ODOO_TEST_BASE_CMD"]


@dataclass(frozen=True)
class SetupInputs:
    docs_root: Path
    source_root: Path
    version: str
    base_cmd: str


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Set up local Claude plugin install and Odoo skill materialization")
    parser.add_argument("--docs-root")
    parser.add_argument("--source-root")
    parser.add_argument("--version")
    parser.add_argument("--python-bin", default="python3")
    parser.add_argument("--odoo-bin")
    parser.add_argument("--config")
    parser.add_argument("--base-cmd")
    parser.add_argument("--yes", action="store_true")
    parser.add_argument("--uninstall", action="store_true")
    return parser.parse_args(argv)


def prompt_required(value: str | None, prompt: str, *, allow_prompt: bool) -> str:
    if value:
        return value
    if not allow_prompt:
        raise SystemExit(f"{prompt} is required in non-interactive mode")
    entered = input(f"{prompt}: ").strip()
    if not entered:
        raise SystemExit(f"{prompt} is required")
    return entered


def resolve_existing_path(raw: str, label: str) -> Path:
    path = Path(raw).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"{label} not found: {path}")
    return path


def build_base_cmd(python_bin: str, odoo_bin: str, config_path: str) -> str:
    return f"{python_bin} {odoo_bin} -c {config_path}"


def load_json_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_file(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def merge_settings_local(existing: dict[str, Any], base_cmd: str) -> dict[str, Any]:
    data = dict(existing)
    env = dict(data.get("env") or {})
    env["ODOO_TEST_BASE_CMD"] = base_cmd
    data["env"] = env
    return data


def remove_managed_settings(existing: dict[str, Any], managed_keys: list[str]) -> dict[str, Any]:
    data = dict(existing)
    env = dict(data.get("env") or {})
    if "env.ODOO_TEST_BASE_CMD" in managed_keys:
        env.pop("ODOO_TEST_BASE_CMD", None)
    if env:
        data["env"] = env
    else:
        data.pop("env", None)
    return data


def collect_setup_inputs(repo_root: Path, args: argparse.Namespace) -> SetupInputs:
    allow_prompt = not args.yes
    docs_root = resolve_existing_path(
        prompt_required(args.docs_root, "Odoo documentation root", allow_prompt=allow_prompt),
        "Docs root",
    )
    source_root = resolve_existing_path(
        prompt_required(args.source_root, "Odoo source root", allow_prompt=allow_prompt),
        "Source root",
    )

    if args.version:
        version = args.version
    else:
        try:
            version, _ = resolve_series(None, docs_root, source_root)
        except SystemExit:
            version = prompt_required(None, "Odoo version", allow_prompt=allow_prompt)

    if args.base_cmd:
        base_cmd = args.base_cmd
    else:
        python_bin = prompt_required(args.python_bin or "python3", "Python executable", allow_prompt=allow_prompt)
        odoo_bin = resolve_existing_path(
            prompt_required(args.odoo_bin, "odoo-bin path", allow_prompt=allow_prompt),
            "odoo-bin",
        )
        config_path = resolve_existing_path(
            prompt_required(args.config, "Odoo config path", allow_prompt=allow_prompt),
            "Config path",
        )
        base_cmd = build_base_cmd(python_bin, str(odoo_bin), str(config_path))

    return SetupInputs(docs_root=docs_root, source_root=source_root, version=version, base_cmd=base_cmd)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.uninstall:
        return 0
    collect_setup_inputs(Path(__file__).resolve().parents[1], args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run the helper tests again**

Run: `python3 -m unittest tests.unit.test_setup_local.SetupLocalHelpersTests -v`
Expected: PASS with all four helper tests reporting `ok`

- [ ] **Step 5: Commit the setup-local helper layer**

```bash
git add tooling/setup_local.py tests/unit/test_setup_local.py
git commit -m "feat: add setup-local helpers"
```

### Task 3: Orchestrate setup and uninstall with mocked CLI tests

**Files:**
- Modify: `tooling/setup_local.py:1-200`
- Modify: `tests/unit/test_setup_local.py:1-120`

- [ ] **Step 1: Extend `tests/unit/test_setup_local.py` with failing orchestration tests**

Add these imports near the top of the file:

```python
import json
import subprocess

from tooling.materialization.materialize_odoo_skill_paths import MaterializationResult
```

Append this second test class to the file:

```python
class SetupLocalCommandFlowTests(unittest.TestCase):
    def test_run_setup_writes_local_state_and_calls_claude_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs_root = root / "docs-18.0"
            source_root = root / "odoo-18.0"
            config_path = root / ".claude" / "odoo-skill-paths.json"
            settings_path = root / ".claude" / "settings.local.json"
            for path in (docs_root, source_root, root / ".claude" / "skills", root / "dist"):
                path.mkdir(parents=True, exist_ok=True)
            args = setup_local.parse_args(
                [
                    "--docs-root",
                    str(docs_root),
                    "--source-root",
                    str(source_root),
                    "--version",
                    "18.0",
                    "--python-bin",
                    "python3",
                    "--odoo-bin",
                    str(source_root / "odoo-bin"),
                    "--config",
                    str(root / "odoo.conf"),
                    "--yes",
                ]
            )
            (source_root / "odoo-bin").write_text("", encoding="utf-8")
            (root / "odoo.conf").write_text("[options]\n", encoding="utf-8")

            commands = []

            def fake_run(command, check=False, cwd=None, text=True, capture_output=True):
                commands.append(command)
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

            def fake_materialize(**kwargs):
                config_path.parent.mkdir(parents=True, exist_ok=True)
                config_path.write_text(
                    json.dumps(
                        {
                            "docsRoot": str(docs_root),
                            "sourceRoot": str(source_root),
                            "version": "18.0",
                            "majorVersion": "18",
                            "versionSource": "--version",
                            "skillsRoot": str(root / ".claude" / "skills"),
                            "materializedAt": "2026-04-20T00:00:00+00:00",
                            "mode": "initial",
                            "materializedFiles": [".claude/skills/odoo-paths.md"],
                        }
                    ),
                    encoding="utf-8",
                )
                return MaterializationResult(
                    changed_files=[root / ".claude" / "skills" / "odoo-paths.md"],
                    version="18.0",
                    major_version="18",
                    version_source="--version",
                    config_path=config_path,
                )

            with patch("tooling.setup_local.shutil.which", return_value="/usr/bin/claude"), patch(
                "tooling.setup_local.build_marketplace",
                side_effect=lambda repo_root, output_dir: output_dir,
            ), patch("tooling.setup_local.materialize_skills", side_effect=fake_materialize), patch(
                "tooling.setup_local.subprocess.run",
                side_effect=fake_run,
            ):
                exit_code = setup_local.run_setup(root, args)

            self.assertEqual(exit_code, 0)
            self.assertEqual(
                commands,
                [
                    ["claude", "plugin", "validate", str(root / "dist" / "marketplace")],
                    ["claude", "plugin", "marketplace", "add", str(root / "dist" / "marketplace")],
                    ["claude", "plugin", "install", "odoo-skills@odoo-skills-dev", "--scope", "local"],
                ],
            )
            settings = json.loads(settings_path.read_text(encoding="utf-8"))
            self.assertEqual(
                settings["env"]["ODOO_TEST_BASE_CMD"],
                f"python3 {source_root / 'odoo-bin'} -c {root / 'odoo.conf'}",
            )

    def test_add_marketplace_retries_with_remove_when_marketplace_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            marketplace_path = root / "dist" / "marketplace"
            marketplace_path.mkdir(parents=True)
            responses = [
                subprocess.CompletedProcess(
                    ["claude", "plugin", "marketplace", "add", str(marketplace_path)],
                    1,
                    stdout="",
                    stderr="Marketplace odoo-skills-dev already exists",
                ),
                subprocess.CompletedProcess(
                    ["claude", "plugin", "marketplace", "remove", "odoo-skills-dev"],
                    0,
                    stdout="",
                    stderr="",
                ),
                subprocess.CompletedProcess(
                    ["claude", "plugin", "marketplace", "add", str(marketplace_path)],
                    0,
                    stdout="",
                    stderr="",
                ),
            ]
            with patch("tooling.setup_local.subprocess.run", side_effect=responses):
                setup_local.add_marketplace(root, marketplace_path)

    def test_run_uninstall_restores_recorded_files_and_cleans_settings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tracked_file = root / ".claude" / "skills" / "odoo-paths.md"
            tracked_file.parent.mkdir(parents=True, exist_ok=True)
            tracked_file.write_text("materialized", encoding="utf-8")
            settings_path = root / ".claude" / "settings.local.json"
            settings_path.write_text(
                json.dumps({"env": {"ODOO_TEST_BASE_CMD": "cmd", "KEEP_ME": "1"}}),
                encoding="utf-8",
            )
            config_path = root / ".claude" / "odoo-skill-paths.json"
            config_path.write_text(
                json.dumps(
                    {
                        "materializedFiles": [".claude/skills/odoo-paths.md"],
                        "setupManagedSettingsKeys": ["env.ODOO_TEST_BASE_CMD"],
                        "pluginName": "odoo-skills",
                        "marketplaceName": "odoo-skills-dev",
                        "installScope": "local",
                        "marketplacePath": str(root / "dist" / "marketplace"),
                    }
                ),
                encoding="utf-8",
            )
            (root / "dist" / "marketplace").mkdir(parents=True)
            commands = []

            def fake_run(command, check=False, cwd=None, text=True, capture_output=True):
                commands.append(command)
                if command[:4] == ["git", "-C", str(root), "show"]:
                    return subprocess.CompletedProcess(command, 0, stdout="Docs: <ODOO_DOCS_ROOT>\n", stderr="")
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

            args = setup_local.parse_args(["--uninstall"])
            with patch("tooling.setup_local.shutil.which", return_value="/usr/bin/claude"), patch(
                "tooling.setup_local.subprocess.run",
                side_effect=fake_run,
            ):
                exit_code = setup_local.run_uninstall(root, args)

            self.assertEqual(exit_code, 0)
            self.assertEqual(
                commands[:2],
                [
                    ["claude", "plugin", "uninstall", "odoo-skills", "--scope", "local"],
                    ["claude", "plugin", "marketplace", "remove", "odoo-skills-dev"],
                ],
            )
            self.assertEqual(json.loads(settings_path.read_text(encoding="utf-8")), {"env": {"KEEP_ME": "1"}})
            self.assertEqual(tracked_file.read_text(encoding="utf-8"), "Docs: <ODOO_DOCS_ROOT>\n")
            self.assertFalse(config_path.exists())
            self.assertFalse((root / "dist" / "marketplace").exists())
```

- [ ] **Step 2: Run the extended setup-local tests to confirm orchestration functions are missing**

Run: `python3 -m unittest tests.unit.test_setup_local -v`
Expected: FAIL with `AttributeError` for `run_setup`, `add_marketplace`, or `run_uninstall`

- [ ] **Step 3: Implement setup and uninstall orchestration in `tooling/setup_local.py`**

Add these imports near the top of the file:

```python
import shutil
import subprocess
from datetime import datetime, timezone

from tooling.build_plugin import build_marketplace
from tooling.materialization.materialize_odoo_skill_paths import materialize_skills
```

Add these functions below `collect_setup_inputs()`:

```python
def ensure_claude_cli() -> None:
    if shutil.which("claude"):
        return
    raise SystemExit("claude CLI is required on PATH")


def run_command(repo_root: Path, command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=False, cwd=repo_root, text=True, capture_output=True)


def update_setup_state(config_path: Path, **fields: Any) -> None:
    config = load_json_file(config_path)
    config.update(fields)
    write_json_file(config_path, config)


def add_marketplace(repo_root: Path, marketplace_path: Path) -> None:
    add_command = ["claude", "plugin", "marketplace", "add", str(marketplace_path)]
    result = run_command(repo_root, add_command)
    if result.returncode == 0:
        return

    combined_output = f"{result.stdout}\n{result.stderr}"
    if "already exists" not in combined_output:
        raise SystemExit(combined_output.strip())

    remove_result = run_command(repo_root, ["claude", "plugin", "marketplace", "remove", MARKETPLACE_NAME])
    if remove_result.returncode != 0:
        raise SystemExit(f"Failed to remove existing marketplace {MARKETPLACE_NAME}")

    retry = run_command(repo_root, add_command)
    if retry.returncode != 0:
        raise SystemExit((retry.stdout or retry.stderr).strip())


def restore_materialized_files(repo_root: Path, relative_paths: list[str]) -> None:
    for relative_path in relative_paths:
        result = run_command(repo_root, ["git", "-C", str(repo_root), "show", f"HEAD:{relative_path}"])
        if result.returncode != 0:
            continue
        target = repo_root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(result.stdout, encoding="utf-8")


def run_setup(repo_root: Path, args: argparse.Namespace) -> int:
    ensure_claude_cli()
    inputs = collect_setup_inputs(repo_root, args)

    settings_path = repo_root / ".claude" / "settings.local.json"
    settings_payload = merge_settings_local(load_json_file(settings_path), inputs.base_cmd)
    write_json_file(settings_path, settings_payload)

    materialization = materialize_skills(
        docs_root=inputs.docs_root,
        source_root=inputs.source_root,
        skills_root=repo_root / ".claude" / "skills",
        config_path=repo_root / ".claude" / "odoo-skill-paths.json",
        version=inputs.version,
        force=True,
        extra_metadata={
            "setupManagedSettingsKeys": MANAGED_SETTINGS_KEYS,
            "pluginName": PLUGIN_NAME,
            "marketplaceName": MARKETPLACE_NAME,
            "installScope": INSTALL_SCOPE,
            "marketplacePath": str(repo_root / "dist" / "marketplace"),
        },
    )

    marketplace_path = build_marketplace(repo_root, repo_root / "dist" / "marketplace")
    validate = run_command(repo_root, ["claude", "plugin", "validate", str(marketplace_path)])
    if validate.returncode != 0:
        raise SystemExit((validate.stdout or validate.stderr).strip())

    add_marketplace(repo_root, marketplace_path)

    install = run_command(
        repo_root,
        ["claude", "plugin", "install", f"{PLUGIN_NAME}@{MARKETPLACE_NAME}", "--scope", INSTALL_SCOPE],
    )
    if install.returncode != 0:
        raise SystemExit((install.stdout or install.stderr).strip())

    update_setup_state(
        materialization.config_path,
        setupCompletedAt=datetime.now(timezone.utc).isoformat(),
    )

    print(f"Installed {PLUGIN_NAME} in {INSTALL_SCOPE} scope")
    print(f"Detected Odoo version {materialization.version}")
    print(f"Wrote {materialization.config_path}")
    print(f"Wrote {settings_path}")
    print("Uninstall: python3 tooling/setup_local.py --uninstall")
    return 0


def run_uninstall(repo_root: Path, args: argparse.Namespace) -> int:
    state_path = repo_root / ".claude" / "odoo-skill-paths.json"
    state = load_json_file(state_path)

    if shutil.which("claude"):
        run_command(repo_root, ["claude", "plugin", "uninstall", state.get("pluginName", PLUGIN_NAME), "--scope", state.get("installScope", INSTALL_SCOPE)])
        run_command(repo_root, ["claude", "plugin", "marketplace", "remove", state.get("marketplaceName", MARKETPLACE_NAME)])

    restore_materialized_files(repo_root, list(state.get("materializedFiles", [])))

    settings_path = repo_root / ".claude" / "settings.local.json"
    if settings_path.exists():
        updated = remove_managed_settings(load_json_file(settings_path), list(state.get("setupManagedSettingsKeys", MANAGED_SETTINGS_KEYS)))
        if updated:
            write_json_file(settings_path, updated)
        else:
            settings_path.unlink()

    marketplace_path = Path(str(state.get("marketplacePath", repo_root / "dist" / "marketplace")))
    if marketplace_path.exists():
        shutil.rmtree(marketplace_path)

    if state_path.exists():
        state_path.unlink()

    print("Removed local setup")
    return 0
```

Replace `main()` with:

```python
def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(__file__).resolve().parents[1]
    if args.uninstall:
        return run_uninstall(repo_root, args)
    return run_setup(repo_root, args)
```

- [ ] **Step 4: Run the full setup-local test module again**

Run: `python3 -m unittest tests.unit.test_setup_local -v`
Expected: PASS with helper and command-flow tests all reporting `ok`

- [ ] **Step 5: Verify the new script exposes the command surface**

Run: `python3 tooling/setup_local.py --help`
Expected: output starts with `usage: setup_local.py` and lists `--docs-root`, `--source-root`, `--python-bin`, `--odoo-bin`, `--config`, `--base-cmd`, `--yes`, and `--uninstall`

- [ ] **Step 6: Commit the orchestrated setup and uninstall flow**

```bash
git add tooling/setup_local.py tests/unit/test_setup_local.py
git commit -m "feat: orchestrate local setup install flow"
```

### Task 4: Switch docs and hook guidance to the one-command flow

**Files:**
- Modify: `README.md:1-26`
- Modify: `.claude/skills/odoo-paths.md:1-48`
- Modify: `tooling/materialization/suggest_odoo_skill_setup.py:1-138`
- Modify: `.claude/skills/scripts/suggest_odoo_skill_setup.py:1-138`
- Modify: `tests/unit/test_plugin_foundation.py:1-47`
- Modify: `tests/unit/test_suggest_odoo_skill_setup.py:1-68`

- [ ] **Step 1: Update the README and hook-guidance tests first**

Replace `test_readme_mentions_plugin_install_flow()` in `tests/unit/test_plugin_foundation.py` with:

```python
def test_readme_mentions_one_command_local_setup(self) -> None:
    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    self.assertIn("python3 tooling/setup_local.py", readme_text)
    self.assertIn("python3 tooling/setup_local.py --uninstall", readme_text)
    self.assertIn("odoo-skills@odoo-skills-dev", readme_text)
```

Replace `test_setup_guidance_points_to_tooling_materialization_script()` in `tests/unit/test_suggest_odoo_skill_setup.py` with:

```python
def test_setup_guidance_points_to_one_command_setup(self) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo_root = Path(tmp)

        message = build_system_message(
            raw="create new odoo module",
            repo_root=repo_root,
            mode="prompt-submit",
        )

        self.assertIn("python3 tooling/setup_local.py", message)
        self.assertIn("Manual fallback:", message)
        self.assertIn("python3 tooling/materialization/materialize_odoo_skill_paths.py", message)
```

Append this test to the same file:

```python
def test_project_copy_guidance_points_to_setup_local_command(self) -> None:
    project_copy = (ROOT / ".claude" / "skills" / "scripts" / "suggest_odoo_skill_setup.py").read_text(encoding="utf-8")
    self.assertIn("python3 tooling/setup_local.py", project_copy)
    self.assertIn("python3 .claude/skills/scripts/materialize_odoo_skill_paths.py", project_copy)
```

- [ ] **Step 2: Run the README and guidance tests to confirm docs still point to the old flow**

Run: `python3 -m unittest tests.unit.test_plugin_foundation tests.unit.test_suggest_odoo_skill_setup -v`
Expected: FAIL because README and hook messages still reference the longer manual materialization path only

- [ ] **Step 3: Rewrite README, path setup docs, and hook messages**

Replace `README.md` with:

```markdown
# odoo-skills

Public Claude Code plugin for Odoo-focused skills.

## Local setup

Clone this repository and run one command:

```bash
git clone git@github.com:vdx-vn/ai-agent
cd ai-agent
python3 tooling/setup_local.py
```

The setup command prompts for:

- Odoo documentation repo root
- Odoo source repo root
- Odoo version when auto-detection cannot resolve it
- either `odoo-bin` and `odoo.conf`, or a full `ODOO_TEST_BASE_CMD`

## Non-interactive setup

```bash
python3 tooling/setup_local.py \
  --docs-root /path/to/odoo/documentation \
  --source-root /path/to/odoo/odoo \
  --python-bin python3 \
  --odoo-bin /path/to/odoo/odoo-bin \
  --config /path/to/odoo.conf \
  --yes
```

## Uninstall local setup

```bash
python3 tooling/setup_local.py --uninstall
```

## Advanced manual fallback

Run Claude Code with this repository as a local plugin source, plus default claude plugin sources:

```bash
claude --plugin-dir ~/.claude/plugins --plugin-dir .
```

Materialize local Odoo paths manually:

```bash
python3 tooling/materialization/materialize_odoo_skill_paths.py --docs-root /path/to/odoo/documentation --source-root /path/to/odoo/source
```

Add the local marketplace and install this plugin from it:

```bash
claude plugin marketplace add ./
claude plugin install odoo-skills@odoo-skills-dev --scope local
```
```

Replace `make_message()` in `tooling/materialization/suggest_odoo_skill_setup.py` with:

```python
def make_message(project_root: Path) -> str:
    return (
        "Detected new Odoo project setup context. From project root, run:\n"
        "`python3 tooling/setup_local.py`\n"
        "That command can prompt for Odoo docs and source roots, detect version when possible, write `.claude/odoo-skill-paths.json`, merge `.claude/settings.local.json`, and install the local plugin.\n"
        "Manual fallback: `python3 tooling/materialization/materialize_odoo_skill_paths.py --docs-root /path/to/odoo/documentation --source-root /path/to/odoo/source`\n"
        "Shared setup guide: `.claude/skills/odoo-paths.md`"
    )
```

Replace `make_message()` in `.claude/skills/scripts/suggest_odoo_skill_setup.py` with:

```python
def make_message(project_root: Path) -> str:
    return (
        "Detected new Odoo project setup context. From project root, run:\n"
        "`python3 tooling/setup_local.py`\n"
        "That command can prompt for Odoo docs and source roots, detect version when possible, write `.claude/odoo-skill-paths.json`, merge `.claude/settings.local.json`, and install the local plugin.\n"
        "Manual fallback: `python3 .claude/skills/scripts/materialize_odoo_skill_paths.py --docs-root /path/to/odoo/documentation --source-root /path/to/odoo/source`\n"
        "Shared setup guide: `.claude/skills/odoo-paths.md`"
    )
```

Replace `.claude/skills/odoo-paths.md` with:

```markdown
# Odoo Path Setup

## Recommended workflow

From repository root, run:

`python3 tooling/setup_local.py`

This command can:

- prompt for Odoo documentation and source repo roots
- detect Odoo version when git branches or path names expose it
- write `.claude/odoo-skill-paths.json`
- materialize the copied `.claude/skills/` tree with concrete paths
- merge `.claude/settings.local.json` with `ODOO_TEST_BASE_CMD`
- install the local plugin into Claude from this repository

## Non-interactive example

`python3 tooling/setup_local.py --docs-root /path/to/odoo/documentation --source-root /path/to/odoo/source --python-bin python3 --odoo-bin /path/to/odoo/source/odoo-bin --config /path/to/odoo.conf --yes`

## Manual fallback

If you only want path materialization, run:

`python3 .claude/skills/scripts/materialize_odoo_skill_paths.py --docs-root /path/to/odoo/documentation --source-root /path/to/odoo/source`

The script auto-detects Odoo version from git branch names or repo path names when possible; otherwise pass `--version 18.0` or another supported series.

## Placeholder meanings

- `<ODOO_DOCS_ROOT>` = absolute path to the local Odoo documentation clone
- `<ODOO_SOURCE_ROOT>` = absolute path to the local Odoo source clone
- `<ODOO_SERIES>` = Odoo series like `17.0`, `18.0`, or `19.0`
- `<ODOO_MAJOR_VERSION>` = major version like `17`, `18`, or `19`

## Local test harness config

For each Odoo project, keep the local base test command in `.claude/settings.local.json`:

```json
{
  "env": {
    "ODOO_TEST_BASE_CMD": "/path/to/python /path/to/odoo-bin -c /path/to/odoo.conf"
  }
}
```

`odoo-local-test-harness` treats this as the immutable base command, then appends `-d`, `--test-tags`, `--test-enable`, `-i` or `-u`, and `--stop-after-init` safely.
Keep this file local and uncommitted.
```

- [ ] **Step 4: Run the updated README and guidance tests again**

Run: `python3 -m unittest tests.unit.test_plugin_foundation tests.unit.test_suggest_odoo_skill_setup -v`
Expected: PASS with README and setup-guidance tests all reporting `ok`

- [ ] **Step 5: Run the focused regression suite for the new flow**

Run: `python3 -m unittest tests.unit.test_materialize_odoo_skill_paths tests.unit.test_setup_local tests.unit.test_suggest_odoo_skill_setup tests.unit.test_plugin_foundation -v`
Expected: PASS with `OK`

- [ ] **Step 6: Run the full repository test suite and plugin validator**

Run: `python3 -m unittest discover -s tests -p 'test_*.py' -v && python3 -m tooling.cli verify && python3 -m tooling.cli build`
Expected: full test suite ends with `OK`, verify exits `0` with no validation errors, and build recreates `dist/marketplace`

- [ ] **Step 7: Commit the onboarding and guidance changes**

```bash
git add README.md .claude/skills/odoo-paths.md tooling/materialization/suggest_odoo_skill_setup.py .claude/skills/scripts/suggest_odoo_skill_setup.py tests/unit/test_plugin_foundation.py tests/unit/test_suggest_odoo_skill_setup.py
git commit -m "docs: switch onboarding to setup-local"
```

## Self-Review Checklist

- **Spec coverage:**
  - one-command direct entrypoint: Task 2 and Task 3
  - interactive prompting and non-interactive flags: Task 2
  - materialization reuse and richer metadata: Task 1
  - `ODOO_TEST_BASE_CMD` merge and cleanup: Task 2 and Task 3
  - marketplace add, validate, install, uninstall: Task 3
  - updated docs and hook guidance: Task 4
  - idempotent rerun behavior: Task 3 `add_marketplace()` retry path and forced rematerialization
  - verification and build regression: Task 4
- **Placeholder scan:** no `TODO`, `TBD`, or unresolved placeholder instructions remain in this plan.
- **Type consistency:** `MaterializationResult`, `SetupInputs`, `materialize_skills()`, `run_setup()`, `run_uninstall()`, `merge_settings_local()`, and `remove_managed_settings()` use the same names in tests and implementation steps.
