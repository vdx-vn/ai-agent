# Overview

Paths below are relative to:
- Docs repo: `<ODOO_DOCS_ROOT>`
- Source repo: `<ODOO_SOURCE_ROOT>`

## Project-local path resolution
Before using docs or source anchors, search upward from the current working directory for `.odoo-skills/project.json`. If it exists, read `docsRoot` as the Odoo docs tree and `sourceRoot` as the Odoo CE source tree. Prefer `.odoo-skills/project.json` over Docker Compose files, module READMEs, or ad hoc filesystem searches. If the config is absent, use the materialized placeholders above or ask for explicit roots.

## Primary routing rule
Use this skill only when the primary requested output is a retrospective or lessons learned artifact after work already happened.

Resolve the roots above from project setup first. All anchors below are relative to those roots. See `../../odoo-paths.md` for shared setup.

## Scope
Produce a retrospective for completed Odoo work, covering what happened, what was missed, and what follow-up actions remain.

## Primary artifact
Retrospective with lessons, remaining gaps, and concrete follow-up actions.

## Key checks
- Compare intended change with observed outcome.
- Identify missing tests, missing safeguards, or misunderstood process assumptions.
- Capture cross-app lessons for future work.
- Produce concrete next actions, not vague commentary.

## Key docs anchors
- `content/contributing/development.rst`
- `content/developer/tutorials/unit_tests.rst`
- `content/administration/upgrade.rst`
- `content/contributing/development/coding_guidelines.rst`

## Key source anchors
- `odoo/tests/common.py`
- `addons/sale_stock/tests`
- `addons/stock_account/models/stock_move.py`

## Frequent sibling skills
- `odoo-review`
- `odoo-test`
