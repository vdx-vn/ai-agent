#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from tooling.local_setup_common import repo_looks_odoo

PROMPT_PATTERNS = [
    r"\bnew\s+odoo\s+(project|addon|module)\b",
    r"\bsetup\s+(an?\s+)?(new\s+)?odoo\b",
    r"\bstart\s+(an?\s+)?(new\s+)?odoo\b",
    r"\bbootstrap\s+(an?\s+)?(new\s+)?odoo\b",
    r"\bcreate\s+(an?\s+)?(new\s+)?odoo\s+(project|addon|module)\b",
    r"\binit(ialize)?\s+(an?\s+)?(new\s+)?odoo\s+(project|addon|module)\b",
]

ODOO_TEST_BASE_CMD_ENV = "ODOO_TEST_BASE_CMD"


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

def make_message(project_root: Path) -> str:
    del project_root
    return (
        "Detected new Odoo project setup context. Install repo entrypoints first with `python3 -m pip install -e .`.\n"
        "From project root, run `odoo-skills project-setup`.\n"
        "If `odoo-skills` is not on PATH, use `python3 -m tooling.cli project-setup`.\n"
        "This writes `.claude/odoo-skill-paths.json` and `.claude/settings.local.json` for this project only, including `ODOO_TEST_BASE_CMD`.\n"
        "Shared setup guide: `.claude/skills/odoo-paths.md`"
    )


def load_settings_local_env(repo_root: Path) -> dict[str, str]:
    settings_path = repo_root / ".claude" / "settings.local.json"
    if not settings_path.exists():
        return {}
    try:
        data = json.loads(settings_path.read_text())
    except json.JSONDecodeError:
        return {}
    env = data.get("env", {})
    return env if isinstance(env, dict) else {}


def malformed_settings_local_json(repo_root: Path) -> bool:
    settings_path = repo_root / ".claude" / "settings.local.json"
    if not settings_path.exists():
        return False
    try:
        json.loads(settings_path.read_text())
    except json.JSONDecodeError:
        return True
    return False


def missing_odoo_test_base_command(repo_root: Path) -> bool:
    value = str(load_settings_local_env(repo_root).get(ODOO_TEST_BASE_CMD_ENV, "")).strip()
    return not value


def make_harness_message() -> str:
    return (
        "Detected Odoo project without local test command. Add this to `.claude/settings.local.json`:\n"
        "```json\n{\n  \"env\": {\n    \"ODOO_TEST_BASE_CMD\": \"/path/to/python /path/to/odoo-bin -c /path/to/odoo.conf\"\n  }\n}\n```\n"
        "Then `odoo-local-test-harness` can append database names, test tags, install or update flags, and `--stop-after-init` automatically."
    )


def make_malformed_harness_message() -> str:
    return (
        "Detected malformed `.claude/settings.local.json`. Fix the JSON first, then set `ODOO_TEST_BASE_CMD` under `env` for `odoo-local-test-harness`."
    )


def build_system_message(raw: str, repo_root: Path, mode: str) -> str:
    config_path = repo_root / ".claude" / "odoo-skill-paths.json"
    matched = detect_prompt_match(raw)
    odooish = repo_looks_odoo(repo_root)
    should_suggest_path_setup = matched if mode == "prompt-submit" else (matched or odooish)
    should_suggest_harness = odooish and (matched if mode == "prompt-submit" else True)

    messages: list[str] = []
    if not config_path.exists() and should_suggest_path_setup:
        messages.append(make_message(repo_root))
    if should_suggest_harness:
        if malformed_settings_local_json(repo_root):
            messages.append(make_malformed_harness_message())
        elif missing_odoo_test_base_command(repo_root):
            messages.append(make_harness_message())
    return "\n\n".join(messages)


def main() -> int:
    args = parse_args()
    raw = sys.stdin.read()
    repo_root = Path.cwd()
    message = build_system_message(raw, repo_root, args.mode)
    if not message:
        return 0
    payload = {"systemMessage": message}
    sys.stdout.write(json.dumps(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
