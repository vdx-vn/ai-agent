# Overview

Paths below are relative to:
- Docs tree: `current Odoo docs tree`
- Source tree: `current Odoo CE source tree`

## Primary routing rule
Use this skill only when the primary requested output is changed code or config artifacts. If the user is still deciding approach, use `odoo-plan`.

Treat docs anchors as relative to the current Odoo docs tree and source anchors as relative to the current Odoo CE source tree. See `../../odoo-paths.md` for shared setup.

## Scope
Create or modify Odoo code, XML, manifests, security files, and migration stubs according to approved scope and existing conventions.

## Primary artifact
Concrete in-scope code or configuration changes plus noted assumptions and follow-up validation needs.

## Key checks
- Prefer ORM-first patterns over raw SQL.
- Update security artifacts when data visibility changes.
- Keep module boundaries and dependencies tight.
- Avoid speculative abstractions and align with Odoo conventions.

## Key docs anchors
- `content/developer/reference/backend/orm.rst`
- `content/developer/reference/backend/module.rst`
- `content/developer/reference/backend/security.rst`
- `content/contributing/development/coding_guidelines.rst`

## Key source anchors
- `odoo/models.py`
- `odoo/api.py`
- `odoo/fields.py`
- `odoo/http.py`
- `odoo/modules/module.py`

## Frequent sibling skills
- `odoo-orm-modeling`
- `odoo-view-ui`
- `odoo-security`
