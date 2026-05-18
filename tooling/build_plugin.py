from __future__ import annotations

import shutil
from pathlib import Path


RUNTIME_PATHS = (".codex-plugin", ".claude-plugin", "skills", "LICENSE")
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
claude plugin install odoo-skills@odoo-skills-dev --scope local
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


def build_marketplace(root: Path, output_dir: Path) -> Path:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for relative_path in RUNTIME_PATHS:
        source_path = root / relative_path
        destination_path = output_dir / relative_path

        if source_path.is_dir():
            shutil.copytree(source_path, destination_path)
        else:
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, destination_path)

    (output_dir / "README.md").write_text(RUNTIME_README, encoding="utf-8")
    return output_dir
