# Overview

Paths below are relative to:
- Docs repo: `<ODOO_DOCS_ROOT>`
- Source repo: `<ODOO_SOURCE_ROOT>`

## Project-local path resolution
Before using docs or source anchors, search upward from the current working directory for `.odoo-skills/project.json`. If it exists, read `docsRoot` as the Odoo docs tree and `sourceRoot` as the Odoo CE source tree. Prefer `.odoo-skills/project.json` over Docker Compose files, module READMEs, or ad hoc filesystem searches. If the config is absent, use the materialized placeholders above or ask for explicit roots.

## Primary routing rule
Use this skill only when the primary requested output is a model or ORM design decision.

Resolve the roots above from project setup first. All anchors below are relative to those roots. See `../../odoo-paths.md` for shared setup.

## Scope
Guide model, field, API, recordset, and compute or onchange design in Odoo ORM.

## Primary artifact
ORM modeling guidance with field or method recommendations and anti-pattern checks.

## Key checks
- Prefer batch-safe recordset operations.
- Choose stored computes only when query or reporting needs justify it.
- Keep onchange UX-only and constrains business-validity oriented.
- Check multi-company and access implications of field design.

## Key docs anchors
- `content/developer/reference/backend/orm.rst`
- `content/developer/tutorials/server_framework_101/01_architecture.rst`
- `content/contributing/development/coding_guidelines.rst`

## Key source anchors
- `odoo/orm/models.py` (v19 ORM package; `odoo/models.py` removed)
- `odoo/api/__init__.py` (re-export shim; decorators in `odoo/orm/decorators.py`)
- `odoo/orm/fields.py` (plus split files: `fields_relational.py`, `fields_numeric.py`, `fields_temporal.py`, `fields_selection.py`)

## Frequent sibling skills
- `odoo-build`
- `odoo-performance`
- `odoo-security`
