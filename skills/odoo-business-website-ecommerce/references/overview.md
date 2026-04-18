# Overview

Paths below are relative to:
- Docs repo: `<ODOO_DOCS_ROOT>`
- Source repo: `<ODOO_SOURCE_ROOT>`

## Primary routing rule
Use this skill only when the primary entrypoint is page, form, portal, cart, checkout, or online storefront behavior. If the entrypoint is lead, quotation, salesperson action, or backend sales order, use `odoo-business-sales`.

Replace the placeholders above with your local repo paths. All anchors below are relative to those roots. See `../../odoo-paths.md` for shared setup.

## Scope
Explain Odoo website and ecommerce flow across content, forms, cart, checkout, online sales, stock visibility, and CRM capture.

## Primary artifact
Website and ecommerce process map from a public or portal entrypoint, with customer journey, downstream sales flow, and cross-app impacts.

## Key checks
- Identify website entrypoint: page, form, shop, cart, checkout, or portal flow.
- Trace customer action into CRM, sales, stock, and payment flows.
- Mention website_sale, website_sale_stock, or website_crm.
- Call out public access and stock-visibility implications.

## Key docs anchors
- `content/applications/sales.rst`
- `content/applications/inventory_and_mrp/inventory.rst`
- `content/applications/finance.rst`

## Key source anchors
- `addons/website`
- `addons/website_sale/controllers/main.py`
- `addons/website_sale_stock`
- `addons/website_crm/controllers/website_form.py`

## Frequent sibling skills
- `odoo-business-sales`
- `odoo-business-inventory`
- `odoo-view-ui`
- `odoo-security`
