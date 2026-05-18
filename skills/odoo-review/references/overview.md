# Overview

Paths below are relative to:
- Docs repo: `<ODOO_DOCS_ROOT>`
- Source repo: `<ODOO_SOURCE_ROOT>`

## Primary routing rule
Use this skill only when the primary requested output is review findings on an existing artifact. If the user wants executed validation evidence, use `odoo-test`. If the prompt centers on exposure or trust boundaries, compose with or defer to `odoo-security`.

Replace the placeholders above with your local repo paths. All anchors below are relative to those roots. See `../../odoo-paths.md` for shared setup.

## Scope
Review an existing Odoo change artifact for architecture fit, maintainability, correctness, broad risk, and cross-app impact before merge.

## Primary artifact
Structured findings on an existing diff or artifact, separated into required fixes, open risks, and optional improvements.

## Key checks
- Inspect module fit and dependency choices.
- Check security, migration, and performance concerns at review depth.
- Look for cross-app breakage via bridge modules.
- Separate required fixes from optional improvements.

## Key docs anchors
- `content/contributing/development.rst`
- `content/contributing/development/git_guidelines.rst`
- `content/developer/reference/backend/security.rst`
- `content/developer/reference/backend/performance.rst`
- `content/developer/reference/backend/testing.rst`

## Key source anchors
- `odoo/models.py`
- `odoo/http.py`
- `odoo/tests/common.py`
- `odoo/addons/base/models/ir_rule.py`
- `odoo/addons/base/models/ir_model.py`

## Frequent sibling skills
- `odoo-security`
- `odoo-testing-reference`
