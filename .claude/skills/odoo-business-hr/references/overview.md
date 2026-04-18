# Overview

Paths below are relative to:
- Docs repo: current Odoo documentation repository checkout
- Source repo: current Odoo CE source repository checkout

## Primary routing rule
Use this skill only when the primary business entrypoint is employee, contract, attendance, time off, planning, or payroll prerequisite. If the entrypoint is expense claim, expense sheet, reimbursement, or posting, use `odoo-business-expenses`.

Set both roots to your local current Odoo and current Odoo CE checkouts. All anchors below are relative to those roots. See `../../odoo-paths.md` for shared setup.

## Scope
Explain Odoo HR processes around employees, attendances, time off, contracts, payroll prerequisites, and related app interactions.

## Primary artifact
HR process map from a workforce entrypoint, with employee lifecycle touchpoints and cross-app dependencies.

## Key checks
- Identify HR entrypoint: employee, contract, attendance, time off, planning, or payroll prerequisite.
- Trace work-entry and approval implications.
- Mention HR links to timesheets, expenses, and payroll prerequisites.
- Call out role and compliance sensitivities.

## Key docs anchors
- `content/applications/hr.rst`
- `content/applications/hr/payroll.rst`
- `content/applications/services/timesheets.rst`

## Key source anchors
- `addons/hr`
- `addons/hr/models`
- `addons/hr_timesheet`
- `addons/hr_expense`

## Frequent sibling skills
- `odoo-business-timesheet-project-services`
- `odoo-business-expenses`
- `odoo-business-accounting`
