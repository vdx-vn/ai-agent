# Overview

Paths below are relative to:
- Docs repo: current Odoo documentation repository checkout
- Source repo: current Odoo CE source repository checkout

## Project-local path resolution
Before using docs or source anchors, search upward from the current working directory for `.odoo-skills/project.json`. If it exists, read `docsRoot` as the Odoo docs tree and `sourceRoot` as the Odoo CE source tree. Prefer `.odoo-skills/project.json` over Docker Compose files, module READMEs, or ad hoc filesystem searches. If the config is absent, use the materialized placeholders above or ask for explicit roots.

## Primary routing rule
Use this skill only when the primary business entrypoint is receipt, delivery, transfer, route, replenishment, or stock move. If the entrypoint is BoM, MO, work center, routing, or subcontracting, use `odoo-business-manufacturing`.

Set both roots to your local current Odoo and current Odoo CE checkouts. All anchors below are relative to those roots. See `../../odoo-paths.md` for shared setup.

## Scope
Explain Odoo warehouse and stock flows, including routes, replenishment, movement documents, traceability, and valuation touchpoints.

## Primary artifact
Inventory process map from a warehouse or stock-document entrypoint, with route logic, valuation, and cross-app effects.

## Key checks
- Name the stock document type: receipt, delivery, internal transfer, adjustment, or valuation.
- Trace route and replenishment implications.
- Mention bridge addons such as sale_stock, purchase_stock, and stock_account.
- Call out valuation and traceability side effects.

## Key docs anchors
- `content/applications/inventory_and_mrp.rst`
- `content/applications/inventory_and_mrp/inventory/` (subdirectory; inventory.rst is a thin toctree stub in v19)
- `content/applications/finance/accounting.rst`

## Key source anchors
- `addons/stock`
- `addons/stock_account/models/stock_move.py`
- `addons/sale_stock`
- `addons/purchase_stock`

## Frequent sibling skills
- `odoo-business-sales`
- `odoo-business-purchase`
- `odoo-business-accounting`
- `odoo-business-manufacturing`
