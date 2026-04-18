# Overview

Paths below are relative to:
- Docs tree: `current Odoo docs tree`
- Source tree: `current Odoo CE source tree`

## Primary routing rule
Use this skill only when the user wants release readiness or rollout sequencing. If the user needs CLI flag semantics or environment mechanics, hand off to `odoo-delivery-ops`. If the primary issue is data or schema evolution, compose with `odoo-upgrade-migration`.

Treat docs anchors as relative to the current Odoo docs tree and source anchors as relative to the current Odoo CE source tree. See `../../odoo-paths.md` for shared setup.

## Scope
Prepare release readiness for Odoo changes, including go or no-go criteria, staging checks, rollout sequencing, rollback considerations, and production-facing cautions.

## Primary artifact
Go or no-go rollout checklist with staging verification, release sequencing, rollback cautions, and production notes.

## Key checks
- Call out update or install order.
- Check migration, noupdate, and data-shape changes.
- List staging verification for critical workflows.
- Highlight public-route, accounting, inventory, or payroll risk.

## Key docs anchors
- `content/developer/reference/cli.rst`
- `content/administration/odoo_sh/getting_started/branches.rst`
- `content/administration/upgrade.rst`
- `content/developer/howtos/upgrade_custom_db.rst`

## Key source anchors
- `odoo/modules/loading.py`
- `odoo/modules/module.py`
- `odoo/http.py`

## Frequent sibling skills
- `odoo-delivery-ops`
- `odoo-upgrade-migration`
- `odoo-test`
