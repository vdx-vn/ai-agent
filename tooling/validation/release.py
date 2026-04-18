from __future__ import annotations

import re

UNRESOLVED_PLACEHOLDER_RE = re.compile(r"<ODOO_[A-Z0-9_]+>")
TODO_MARKER_RE = re.compile(r"\b(?:TODO|TBD)\b", re.IGNORECASE)


def scan_release_text(text: str) -> list[str]:
    errors: list[str] = []
    if UNRESOLVED_PLACEHOLDER_RE.search(text):
        errors.append("unresolved Odoo placeholder")
    if TODO_MARKER_RE.search(text):
        errors.append("unresolved release marker")
    return errors
