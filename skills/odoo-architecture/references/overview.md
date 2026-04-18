# Overview

Paths below are relative to:
- Docs tree: `current Odoo docs tree`
- Source tree: `current Odoo CE source tree`

## Primary routing rule
Use this skill only when the primary requested output is an addon-placement or dependency decision.

Treat docs anchors as relative to the current Odoo docs tree and source anchors as relative to the current Odoo CE source tree. See `../../odoo-paths.md` for shared setup.

## Scope
Guide module boundaries, dependency graph, inheritance strategy, and bridge-module placement for Odoo addons.

## Primary artifact
Architecture recommendation with target addon, dependency rationale, and bridge-module guidance.

## Key checks
- Check manifest dependencies and auto_install candidates.
- Prefer bridge modules when logic spans stable domains.
- Keep responsibilities cohesive and avoid dumping unrelated logic into a large addon.
- Name upgrade and test implications of placement.

## Key docs anchors
- `content/developer/reference/backend/module.rst`
- `content/developer/tutorials/server_framework_101/01_architecture.rst`
- `content/contributing/development/coding_guidelines.rst`

## Key source anchors
- `odoo/modules/module.py`
- `odoo/modules/loading.py`
- `odoo/modules/registry.py`
- `addons/sale_stock/__manifest__.py`
- `addons/purchase_stock/__manifest__.py`
- `addons/stock_account/__manifest__.py`

## Frequent sibling skills
- `odoo-plan`
- `odoo-build`
