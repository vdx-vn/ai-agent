from __future__ import annotations

import re
from typing import Any

import yaml

ALLOWED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "compatibility",
    "version",
}
KebabNameRe = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_frontmatter(skill_text: str) -> tuple[dict[str, Any] | None, str]:
    if not skill_text.startswith("---\n"):
        return None, skill_text

    end = skill_text.find("\n---\n", 4)
    if end == -1:
        return None, skill_text

    raw_frontmatter = skill_text[4:end]
    body = skill_text[end + 5 :]
    loaded = yaml.safe_load(raw_frontmatter) or {}
    if not isinstance(loaded, dict):
        return None, body
    return loaded, body


def validate_frontmatter(skill_text: str) -> list[str]:
    frontmatter, _ = parse_frontmatter(skill_text)
    if frontmatter is None:
        return ["missing frontmatter"]

    errors: list[str] = []

    unknown = sorted(set(frontmatter.keys()) - ALLOWED_FRONTMATTER_KEYS)
    if unknown:
        errors.append("unsupported frontmatter keys: " + ", ".join(unknown))

    name = str(frontmatter.get("name", "")).strip()
    if not name:
        errors.append("missing frontmatter name")
    elif not KebabNameRe.fullmatch(name):
        errors.append("frontmatter name must be kebab-case")

    description = str(frontmatter.get("description", "")).strip()
    if not description:
        errors.append("missing frontmatter description")

    return errors
