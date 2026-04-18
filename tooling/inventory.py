from __future__ import annotations

import json
from pathlib import Path


def load_inventory(root: Path) -> list[dict[str, object]]:
    inventory_path = root / "docs" / "reference" / "skill-inventory.json"
    data = json.loads(inventory_path.read_text(encoding="utf-8"))

    if not isinstance(data, dict):
        raise ValueError("skill-inventory.json must be a JSON object")

    skills = data.get("skills")
    if not isinstance(skills, list):
        raise ValueError("skill-inventory.json must define a top-level 'skills' list")

    return skills
