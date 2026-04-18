# Overview

Paths below are relative to:
- Docs tree: `current Odoo docs tree`
- Source tree: `current Odoo CE source tree`

## Primary routing rule
Use this skill only when the user wants a plan artifact. If the user wants a risk brief, use `odoo-think`. If the user wants code edits, use `odoo-build`.

Treat docs anchors as relative to the current Odoo docs tree and source anchors as relative to the current Odoo CE source tree. See `../../odoo-paths.md` for shared setup.

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
- `odoo/models.py`
- `odoo/http.py`
- `odoo/tests/common.py`

## Frequent sibling skills
- `odoo-think`
- `odoo-test`
- `odoo-upgrade-migration`
