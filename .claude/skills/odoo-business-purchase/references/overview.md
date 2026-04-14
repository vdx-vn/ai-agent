# Overview

Paths below are relative to:
- Docs repo: `<ODOO_DOCS_ROOT>`
- Source repo: `<ODOO_SOURCE_ROOT>`

## Primary routing rule
Use this skill only when the primary business entrypoint is RFQ, purchase order, replenishment through buying, or vendor-side procurement.

Replace the placeholders above with your local repo paths. All anchors below are relative to those roots. See `../../odoo-paths.md` for shared setup.

## Scope
Explain Odoo purchase lifecycle from RFQ and purchase order through receipt, replenishment, and vendor billing.

## Primary artifact
Purchase process map with entrypoint, downstream documents, roles, and cross-app impacts.

## Key checks
- Identify whether trigger is manual buying, replenishment, or MRP demand.
- Trace PO approval to pickings and bills.
- Name bridge modules such as purchase_stock or purchase_mrp.
- Call out stock, accounting, and approval side effects.

## Key docs anchors
- `content/applications/inventory_and_mrp.rst`
- `content/applications/finance/accounting.rst`
- `content/applications/finance/accounting/taxes.rst`

## Key source anchors
- `addons/purchase`
- `addons/purchase/models/purchase_order.py`
- `addons/purchase_stock/models/purchase_order.py`

## Frequent sibling skills
- `odoo-business-inventory`
- `odoo-business-accounting`
- `odoo-business-manufacturing`
