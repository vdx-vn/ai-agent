# Overview

Paths below are relative to:
- Docs repo: current Odoo documentation repository checkout
- Source repo: current Odoo CE source repository checkout

## Project-local path resolution
Before using docs or source anchors, search upward from the current working directory for `.odoo-skills/project.json`. If it exists, read `docsRoot` as the Odoo docs tree and `sourceRoot` as the Odoo CE source tree. Prefer `.odoo-skills/project.json` over Docker Compose files, module READMEs, or ad hoc filesystem searches. If the config is absent, use the materialized placeholders above or ask for explicit roots.

## Primary routing rule
Use this skill only when the primary business entrypoint is lead, opportunity, quotation, salesperson action, or backend sales order. If the entrypoint is page, form, cart, checkout, or portal, use `odoo-business-website-ecommerce`.

Set both roots to your local current Odoo and current Odoo CE checkouts. All anchors below are relative to those roots. See `../../odoo-paths.md` for shared setup.

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
