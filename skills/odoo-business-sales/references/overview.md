# Overview

Paths below are relative to:
- Docs repo: `<ODOO_DOCS_ROOT>`
- Source repo: `<ODOO_SOURCE_ROOT>`

## Primary routing rule
Use this skill only when the primary business entrypoint is lead, opportunity, quotation, salesperson action, or backend sales order. If the entrypoint is page, form, cart, checkout, or portal, use `odoo-business-website-ecommerce`.

Replace the placeholders above with your local repo paths. All anchors below are relative to those roots. See `../../odoo-paths.md` for shared setup.

## Scope
Explain Odoo backend sales lifecycle and the cross-app links from CRM through quotation, order, delivery, and invoicing.

## Primary artifact
Sales process map from a backend sales entrypoint, with downstream documents, roles, and cross-app impacts.

## Key checks
- Identify entrypoint: lead, opportunity, quote, or backend order.
- Trace downstream logistics and invoicing documents.
- Name bridge modules such as sale_crm, sale_stock, or sale_project.
- Call out pricing, tax, delivery, or project side effects.

## Key docs anchors
- `content/applications/sales.rst`
- `content/applications/sales/sales.rst`
- `content/applications/finance/accounting.rst`

## Key source anchors
- `addons/sale`
- `addons/sale/models/sale_order.py`
- `addons/sale_crm/models/crm_lead.py`
- `addons/sale_stock/models/sale_order.py`

## Frequent sibling skills
- `odoo-business-inventory`
- `odoo-business-accounting`
- `odoo-business-website-ecommerce`
