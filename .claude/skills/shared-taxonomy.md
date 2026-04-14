# Shared Taxonomy

Paths below are relative to:
- Docs repo: `<ODOO_DOCS_ROOT>`
- Source repo: `<ODOO_SOURCE_ROOT>`

## Path placeholders
- See `odoo-paths.md` for shared setup and usage rules.
- `<ODOO_DOCS_ROOT>` = local Odoo documentation clone
- `<ODOO_SOURCE_ROOT>` = local Odoo source clone
- Skill reference paths below are relative to these roots.

## Core Odoo technical terms
- **Addon / module**: installable package with `__manifest__.py`.
- **Bridge module**: addon that connects two business domains, often with `auto_install=True`.
- **ACL**: model-level access control in CSV or ORM metadata.
- **Record rule**: domain-based row-level access filter.
- **ORM**: Odoo recordset and model layer in `odoo/models.py`.
- **QWeb / OWL**: templating and client-side UI systems.
- **noupdate**: data record should not be overwritten on module update.
- **HttpCase / tour**: browser-facing test patterns.

## Primary business entrypoints used for tie-breaking
- Backend sales: opportunity, quotation, salesperson action, backend order
- Website ecommerce: page, public form, portal, cart, checkout
- Inventory: receipt, delivery, transfer, route, replenishment, stock move
- Manufacturing: BoM, MO, work center, routing, subcontracting
- HR: employee, contract, attendance, time off, payroll prerequisite
- Expenses: expense claim, expense sheet, reimbursement, posting

## Core bridge addons to watch
- `sale_stock`
- `purchase_stock`
- `stock_account`
- `mrp_account`
- `sale_mrp`
- `purchase_mrp`
- `sale_crm`
- `sale_project`
- `website_sale_stock`

## Common document chains
- CRM lead or opportunity → quotation → sales order → delivery → invoice
- RFQ → purchase order → receipt → vendor bill
- Manufacturing order → component moves → finished moves → valuation
- Timesheet → sale_project or analytic flow → invoice
- Expense → expense sheet approval → account move or reimbursement
- Website form or cart → lead or order → delivery → invoice

## Shared source anchors
- `odoo/models.py`
- `odoo/api.py`
- `odoo/fields.py`
- `odoo/http.py`
- `odoo/modules/module.py`
- `odoo/modules/loading.py`
- `odoo/modules/registry.py`
- `odoo/tests/common.py`
- `odoo/addons/base/models/ir_rule.py`
- `odoo/addons/base/models/ir_model.py`
- `odoo/addons/base/models/ir_http.py`
