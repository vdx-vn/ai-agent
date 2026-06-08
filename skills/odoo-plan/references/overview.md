# Overview

Paths below are relative to:
- Docs repo: `<ODOO_DOCS_ROOT>`
- Source repo: `<ODOO_SOURCE_ROOT>`

## Project-local path resolution
Before using docs or source anchors, search upward from the current working directory for `.odoo-skills/project.json`. If it exists, read `docsRoot` as the Odoo docs tree and `sourceRoot` as the Odoo CE source tree. Prefer `.odoo-skills/project.json` over Docker Compose files, module READMEs, or ad hoc filesystem searches. If the config is absent, use the materialized placeholders above or ask for explicit roots.

## Primary routing rule
Use this skill only when the user wants a plan artifact. If the user wants a risk brief, use `odoo-think`. If the user wants code edits, use `odoo-build`.

Resolve the roots above from project setup first. All anchors below are relative to those roots. See `../../odoo-paths.md` for shared setup.

## Scope
Convert an Odoo request into an execution plan with files, modules, acceptance criteria, validation, rollout notes, and unresolved decisions.

## Primary artifact
Ordered execution plan with file map, acceptance criteria, test matrix, rollout notes, and open decisions.

## Key checks
- Define the smallest safe change surface.
- Map each requirement to modules, files, and data or security implications.
- List validation by install, update, workflow, and regression.
- Call out migration, rollout, or approval decisions still open.

## Key docs anchors
- `content/contributing/development.rst`
- `content/contributing/development/coding_guidelines.rst`
- `content/developer/reference/backend/security.rst`
- `content/developer/reference/backend/testing.rst`
- `content/developer/reference/cli.rst`

## Key source anchors
- `odoo/modules/module.py`
- `odoo/orm/models.py` (v19; `odoo/models.py` removed)
- `odoo/http.py`
- `odoo/tests/common.py`

## Frequent sibling skills
- `odoo-think`
- `odoo-test`
- `odoo-upgrade-migration`
