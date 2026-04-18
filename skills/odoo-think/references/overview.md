# Overview

Paths below are relative to:
- Docs tree: `current Odoo docs tree`
- Source tree: `current Odoo CE source tree`

## Primary routing rule
Use this skill only when the primary requested output is a scoping brief or impact diagnosis. If the user wants ordered steps, file-by-file actions, or acceptance criteria, hand off to `odoo-plan`.

Treat docs anchors as relative to the current Odoo docs tree and source anchors as relative to the current Odoo CE source tree. See `../../odoo-paths.md` for shared setup.

## Scope
Frame the request, identify impacted modules, business entrypoints, risks, and unknowns before any execution plan or implementation begins.

## Primary artifact
Risk-oriented scoping brief with module map, business entrypoint, cross-app impact, and open questions.

## Key checks
- Classify work as bug, feature, refactor, integration, migration, or ops.
- Identify primary addon, bridge addons, and downstream modules.
- Name the business entrypoint and likely downstream documents.
- Call out unknowns that block planning.

## Key docs anchors
- `content/contributing/development.rst`
- `content/developer/tutorials/server_framework_101/01_architecture.rst`
- `content/developer/reference/backend/module.rst`
- `content/developer/reference/backend/security.rst`

## Key source anchors
- `odoo/modules/module.py`
- `odoo/modules/loading.py`
- `odoo/modules/registry.py`
- `addons/sale_stock/__manifest__.py`
- `addons/purchase_stock/__manifest__.py`
- `addons/stock_account/__manifest__.py`

## Frequent sibling skills
- `odoo-plan`
- `odoo-architecture`
