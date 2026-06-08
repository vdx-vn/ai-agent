# Overview

Paths below are relative to:
- Docs repo: `<ODOO_DOCS_ROOT>`
- Source repo: `<ODOO_SOURCE_ROOT>`

## Project-local path resolution
Before using docs or source anchors, search upward from the current working directory for `.odoo-skills/project.json`. If it exists, read `docsRoot` as the Odoo docs tree and `sourceRoot` as the Odoo CE source tree. Prefer `.odoo-skills/project.json` over Docker Compose files, module READMEs, or ad hoc filesystem searches. If the config is absent, use the materialized placeholders above or ask for explicit roots.

## Primary routing rule
Use this skill only when the primary requested output is migration or upgrade strategy. If the user mainly wants command semantics, use `odoo-delivery-ops`.

Resolve the roots above from project setup first. All anchors below are relative to those roots. See `../../odoo-paths.md` for shared setup.

## Scope
Guide schema and data migration strategy for Odoo changes, including upgrade scripts, noupdate handling, and version transitions.

## Primary artifact
Migration strategy with data-preservation plan, script notes, rollout order, and validation needs.

## Key checks
- Name data preservation strategy explicitly.
- Check noupdate records and XML IDs affected by the change.
- Plan upgrade scripts by phase when needed.
- Require rehearsal and validation for data-shape changes.

## Key docs anchors
- `content/administration/upgrade.rst`
- `content/developer/howtos/upgrade_custom_db.rst`
- `content/developer/reference/upgrades/upgrade_scripts.rst`

## Key source anchors
- `odoo/modules/loading.py`
- `odoo/modules/module.py`
- `addons/stock_account/__manifest__.py`

## Frequent sibling skills
- `odoo-ship`
- `odoo-plan`
- `odoo-delivery-ops`
