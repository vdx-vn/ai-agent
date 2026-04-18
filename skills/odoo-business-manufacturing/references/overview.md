# Overview

Paths below are relative to:
- Docs repo: `<ODOO_DOCS_ROOT>`
- Source repo: `<ODOO_SOURCE_ROOT>`

## Primary routing rule
Use this skill only when the primary business entrypoint is BoM, MO, work center, routing, subcontracting, or production planning. If the entrypoint is warehouse documents or routes without production-control logic, use `odoo-business-inventory`.

Replace the placeholders above with your local repo paths. All anchors below are relative to those roots. See `../../odoo-paths.md` for shared setup.

## Scope
Explain Odoo manufacturing process and its cross-app behavior across stock, procurement, sales, and accounting.

## Primary artifact
Manufacturing process map from a BoM or MO entrypoint, with operations, stock effects, and downstream cross-app impacts.

## Key checks
- Identify BoM, MO, operation, or subcontracting entrypoint.
- Trace raw and finished moves into stock and valuation.
- Name bridge addons such as mrp_account, sale_mrp, or purchase_mrp.
- Call out quality, maintenance, or subassembly side effects when relevant.

## Key docs anchors
- `content/applications/inventory_and_mrp.rst`
- `content/applications/inventory_and_mrp/manufacturing.rst`
- `content/applications/inventory_and_mrp/manufacturing/advanced_configuration/sub_assemblies.rst`

## Key source anchors
- `addons/mrp`
- `addons/mrp/models/mrp_production.py`
- `addons/mrp_account`
- `addons/sale_mrp`
- `addons/purchase_mrp`

## Frequent sibling skills
- `odoo-business-inventory`
- `odoo-business-purchase`
- `odoo-business-sales`
- `odoo-business-accounting`
