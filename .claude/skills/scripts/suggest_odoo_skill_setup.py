#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PROMPT_PATTERNS = [
    r"\bnew\s+odoo\s+(project|addon|module)\b",
    r"\bsetup\s+(an?\s+)?(new\s+)?odoo\b",
    r"\bstart\s+(an?\s+)?(new\s+)?odoo\b",
    r"\bbootstrap\s+(an?\s+)?(new\s+)?odoo\b",
    r"\bcreate\s+(an?\s+)?(new\s+)?odoo\s+(project|addon|module)\b",
    r"\binit(ialize)?\s+(an?\s+)?(new\s+)?odoo\s+(project|addon|module)\b",
]

ODOO_MARKERS = ["odoo-bin", "addons", "odoo"]
MAX_MANIFEST_SCAN_DEPTH = 2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Suggest Odoo skill path setup for new projects")
    parser.add_argument(
        "--mode",
        choices=["session-start", "prompt-submit"],
        default="prompt-submit",
        help="Hook context mode so the script can avoid noisy suggestions",
    )
    return parser.parse_args()


def detect_prompt_match(raw: str) -> bool:
    text = raw.lower()
    return any(re.search(pattern, text) for pattern in PROMPT_PATTERNS)


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


def make_message(project_root: Path) -> str:
    return (
        "Detected new Odoo project setup context. From project root, run:\n"
        "`python3 .claude/skills/scripts/materialize_odoo_skill_paths.py --docs-root /path/to/odoo/documentation --source-root /path/to/odoo/source`\n"
        "The script auto-detects Odoo version from git branch or repo path when possible; otherwise add `--version 18.0` or similar.\n"
        "This will write `.claude/odoo-skill-paths.json` and materialize the copied skill library.\n"
        "Shared setup guide: `.claude/skills/odoo-paths.md`"
    )


def main() -> int:
    args = parse_args()
    raw = sys.stdin.read()
    repo_root = Path.cwd()
    config_path = repo_root / ".claude" / "odoo-skill-paths.json"
    if config_path.exists():
        return 0

    matched = detect_prompt_match(raw)
    odooish = repo_looks_odoo(repo_root)

    should_suggest = matched if args.mode == "prompt-submit" else (matched or odooish)
    if not should_suggest:
        return 0

    payload = {"systemMessage": make_message(repo_root)}
    sys.stdout.write(json.dumps(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
