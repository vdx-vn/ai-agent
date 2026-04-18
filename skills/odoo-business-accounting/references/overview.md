# Overview

Paths below are relative to:
- Docs repo: current Odoo documentation repository checkout
- Source repo: current Odoo CE source repository checkout

## Primary routing rule
Use this skill only when the primary business entrypoint is invoice, bill, payment, tax, reconciliation, localization, or valuation impact.

Set both roots to your local current Odoo and current Odoo CE checkouts. All anchors below are relative to those roots. See `../../odoo-paths.md` for shared setup.

## Scope
Explain Odoo accounting flow and finance implications across invoices, bills, journals, taxes, payments, reconciliation, localization, and valuation.

## Primary artifact
Accounting process map with finance documents, posting impacts, and cross-app implications.

## Key checks
- Identify finance entrypoint: invoice, bill, payment, tax, reconciliation, or valuation.
- Trace upstream business documents and downstream reports.
- Mention crossovers from stock_account, hr_expense, or timesheets when relevant.
- Call out localization and fiscal-position concerns.

## Key docs anchors
- `content/applications/finance.rst`
- `content/applications/finance/accounting.rst`
- `content/applications/finance/accounting/taxes.rst`
- `content/applications/finance/fiscal_localizations.rst`

## Key source anchors
- `addons/account`
- `addons/account/models`
- `addons/stock_account/models/stock_move.py`
- `addons/hr_expense/models/hr_expense_sheet.py`

## Frequent sibling skills
- `odoo-business-sales`
- `odoo-business-purchase`
- `odoo-business-inventory`
- `odoo-business-expenses`
