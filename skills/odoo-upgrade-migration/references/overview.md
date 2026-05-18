# Overview

Paths below are relative to:
- Docs repo: `<ODOO_DOCS_ROOT>`
- Source repo: `<ODOO_SOURCE_ROOT>`

## Primary routing rule
Use this skill only when the primary requested output is migration or upgrade strategy. If the user mainly wants command semantics, use `odoo-delivery-ops`.

Replace the placeholders above with your local repo paths. All anchors below are relative to those roots. See `../../odoo-paths.md` for shared setup.

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
