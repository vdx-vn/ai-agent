from __future__ import annotations

import json
import shutil
from pathlib import Path


PLUGIN_NAME = "odoo-skills-v19"
MARKETPLACE_NAME = "odoo-skills-v19"
PLUGIN_RUNTIME_PATHS = (".codex-plugin", ".claude-plugin/plugin.json", "skills", "LICENSE")
RUNTIME_README = """# odoo-skills Runtime marketplace bundle

Public plugin bundle for Odoo-focused skills.

## Codex CLI

```bash
codex plugin marketplace add ./dist/marketplace
codex
```

## Claude Code

```bash
claude plugin marketplace add ./dist/marketplace
claude plugin install odoo-skills@odoo-skills-v19 --scope local
```

## Optional: configure a local Odoo project

Optional for local Odoo repositories only. These follow-up commands must be run from a clone of the source repository, not from this runtime bundle. Install the repository CLI entrypoints from that separate source-repo clone first, then run project setup in the target Odoo repository:

```bash
python3 -m pip install -e .
odoo-skills project-setup
# fallback
python3 -m tooling.cli project-setup
```

## Runtime contents

This bundle ships Codex and Claude plugin metadata, public skills, and license files only.
Repo-only authoring tools such as tooling/ are not included.
"""


def codex_marketplace(plugin_path: str) -> dict:
    return {
        "name": MARKETPLACE_NAME,
        "interface": {"displayName": "Odoo Skills Dev"},
        "plugins": [
            {
                "name": PLUGIN_NAME,
                "source": {
                    "source": "local",
                    "path": plugin_path,
                },
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Coding",
            }
        ],
    }


def claude_marketplace(plugin_path: str) -> dict:
    return {
        "name": MARKETPLACE_NAME,
        "owner": {"name": "TruongPX"},
        "metadata": {
            "description": "Local development marketplace for the odoo-skills plugin",
            "pluginRoot": plugin_path,
        },
        "plugins": [
            {
                "name": PLUGIN_NAME,
                "source": plugin_path,
                "description": "Odoo-focused skill library",
                "version": "1.0.0",
            }
        ],
    }


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def build_marketplace(root: Path, output_dir: Path) -> Path:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    plugin_root = output_dir / "plugins" / PLUGIN_NAME
    plugin_root.mkdir(parents=True, exist_ok=True)

    for relative_path in PLUGIN_RUNTIME_PATHS:
        source_path = root / relative_path
        destination_path = plugin_root / relative_path

        if source_path.is_dir():
            shutil.copytree(source_path, destination_path)
        else:
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, destination_path)

    write_json(output_dir / ".agents" / "plugins" / "marketplace.json", codex_marketplace(f"./plugins/{PLUGIN_NAME}"))
    write_json(output_dir / ".claude-plugin" / "marketplace.json", claude_marketplace(f"./plugins/{PLUGIN_NAME}"))
    (output_dir / "README.md").write_text(RUNTIME_README, encoding="utf-8")
    shutil.copy2(root / "LICENSE", output_dir / "LICENSE")
    return output_dir
