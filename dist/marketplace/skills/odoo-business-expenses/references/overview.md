# Overview

Paths below are relative to:
- Docs repo: current Odoo documentation repository checkout
- Source repo: current Odoo CE source repository checkout

## Primary routing rule
Use this skill only when the primary business entrypoint is expense claim, expense sheet, reimbursement, or expense posting. If the entrypoint is employee contract, attendance, time off, or payroll prerequisite, use `odoo-business-hr`.

Set both roots to your local current Odoo and current Odoo CE checkouts. All anchors below are relative to those roots. See `../../odoo-paths.md` for shared setup.

## Scope
Explain Odoo expense flow from submission through approval, posting, and reimbursement, including HR and accounting links.

## Primary artifact
Expense process map from an expense-claim entrypoint, with states, roles, accounting impacts, and related HR links.

## Key checks
- Identify expense state and actor: employee, manager, accountant.
- Trace sheet approval to posting and reimbursement.
- Mention HR and accounting dependencies explicitly.
- Call out policy or multi-company implications when relevant.

## Key docs anchors
- `content/applications/finance.rst`
- `content/applications/hr.rst`
- `content/applications/finance/accounting.rst`

## Key source anchors
- `addons/hr_expense`
- `addons/hr_expense/models/hr_expense_sheet.py`
- `addons/account`

## Frequent sibling skills
- `odoo-business-hr`
- `odoo-business-accounting`
- `odoo-security`
