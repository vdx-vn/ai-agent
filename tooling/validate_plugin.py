from __future__ import annotations

from pathlib import Path

from tooling.inventory import load_inventory
from tooling.validation import scan_release_text, validate_frontmatter, validate_layout


def validate_plugin(root: Path) -> list[str]:
    errors: list[str] = []

    for skill in load_inventory(root):
        name = str(skill.get("name", "")).strip()
        if not name:
            continue

        skill_path = root / "skills" / name / "SKILL.md"
        if not skill_path.exists():
            errors.append(f"skills/{name}/SKILL.md: missing file")
            continue

        text = skill_path.read_text(encoding="utf-8")

        for message in validate_frontmatter(text):
            errors.append(f"skills/{name}/SKILL.md: {message}")
        for message in validate_layout(text):
            errors.append(f"skills/{name}/SKILL.md: {message}")
        for message in scan_release_text(text):
            errors.append(f"skills/{name}/SKILL.md: {message}")

    return errors
