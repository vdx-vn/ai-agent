from __future__ import annotations

import re

REQUIRED_SECTIONS = [
    "Purpose",
    "Primary routing rule",
    "Use this skill when",
    "Do not use this skill when",
    "Required inputs",
    "Workflow",
    "Output contract",
]


def validate_layout(skill_text: str) -> list[str]:
    errors: list[str] = []
    for section in REQUIRED_SECTIONS:
        pattern = re.compile(rf"^#\s+{re.escape(section)}\s*$", re.MULTILINE)
        if not pattern.search(skill_text):
            errors.append(f"missing section: # {section}")
    return errors
