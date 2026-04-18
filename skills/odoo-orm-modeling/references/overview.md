# Overview

Paths below are relative to:
- Docs tree: `current Odoo docs tree`
- Source tree: `current Odoo CE source tree`

## Primary routing rule
Use this skill only when the primary requested output is a model or ORM design decision.

Treat docs anchors as relative to the current Odoo docs tree and source anchors as relative to the current Odoo CE source tree. See `../../odoo-paths.md` for shared setup.

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
- `odoo/models.py`
- `odoo/api.py`
- `odoo/fields.py`

## Frequent sibling skills
- `odoo-build`
- `odoo-performance`
- `odoo-security`
