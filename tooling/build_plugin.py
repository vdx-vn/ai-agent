from __future__ import annotations

import shutil
from pathlib import Path


RUNTIME_PATHS = (".claude-plugin", "skills", "LICENSE")
RUNTIME_README = """# odoo-skills Runtime marketplace bundle

Public Claude Code plugin for Odoo-focused skills.

## Install from local marketplace

```bash
claude plugin marketplace add ./
claude plugin install odoo-skills@odoo-skills-dev --scope local
```

Slash-command equivalents:

- /plugin marketplace add
- /plugin install odoo-skills@odoo-skills-dev

## Runtime contents

This marketplace bundle ships plugin metadata, public `skills/`, and license files only.
Repo-only authoring tools such as `tooling/` and `.claude/skills/` are not included in runtime bundle.
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
