from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from tooling.build_plugin import build_marketplace


def _run_command(command: list[str], *, root: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        check=False,
        cwd=root,
        env=env,
        text=True,
        capture_output=True,
    )


def _contains_odoo_skills(payload: Any) -> bool:
    if isinstance(payload, str):
        return payload == "odoo-skills" or payload.split("@", 1)[0] == "odoo-skills"

    if isinstance(payload, list):
        return any(_contains_odoo_skills(item) for item in payload)

    if isinstance(payload, dict):
        return any(_contains_odoo_skills(value) for value in payload.values())

    return False


def smoke_install() -> int:
    root = Path(__file__).resolve().parents[1]
    marketplace_root = build_marketplace(root, root / "dist" / "marketplace")

    with tempfile.TemporaryDirectory(prefix="odoo-skills-smoke-home-") as temp_home:
        env = os.environ.copy()
        env["HOME"] = temp_home

        commands = [
            ["claude", "plugin", "validate", str(marketplace_root)],
            ["claude", "plugin", "marketplace", "add", str(marketplace_root)],
            ["claude", "plugin", "install", "odoo-skills@odoo-skills-dev", "--scope", "local"],
            ["claude", "plugin", "list", "--json"],
        ]

        list_result: subprocess.CompletedProcess[str] | None = None
        for command in commands:
            result = _run_command(command, root=root, env=env)
            if result.returncode != 0:
                return result.returncode
            if command[-1] == "--json":
                list_result = result

    if list_result is None:
        return 1

    try:
        payload = json.loads(list_result.stdout)
    except json.JSONDecodeError:
        return 1

    return 0 if _contains_odoo_skills(payload) else 1
