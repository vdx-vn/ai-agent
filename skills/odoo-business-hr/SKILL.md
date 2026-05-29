---
name: odoo-business-hr
description: "Explain Odoo HR processes across employees, contracts, attendances, time off, payroll prerequisites, and related HR app interactions. Use when the primary entrypoint is employee, contract, attendance, time off, or workforce policy, not an expense claim lifecycle."
---

# Purpose
Explain Odoo HR processes around employees, attendances, time off, contracts, payroll prerequisites, and related app interactions.

# Primary routing rule
Use this skill only when the primary business entrypoint is employee, contract, attendance, time off, planning, or payroll prerequisite. If the entrypoint is expense claim, expense sheet, reimbursement, or posting, use `odoo-business-expenses`.

# Use this skill when
- explain employee, attendance, time-off, or HR-process impact
- reason about payroll prerequisites or work-entry inputs
- map HR app interactions around employee data and policy

# Do not use this skill when
- the primary entrypoint is expense claim lifecycle
- the request is project or service billing only
- the issue is technical security or ORM design

# Required inputs
Question or artifact, module/entrypoint if known, surrounding context when available.

# Workflow
Confirm → Read anchors → Apply checklist → Answer with guidance → State boundary decision.

# Output contract
- base HR flow
- cross-app impacts
- roles and decision points
- golden-path test ideas
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only this skill's domain. Anchor to Odoo docs + CE source, not generic ERP intuition.
- Highlight cross-app, accounting, or security effects. Redirect to task skills for planning/building/testing/shipping.

# Must hand off when
- If the entrypoint is expense claim, sheet approval, reimbursement, or posting, hand off to `odoo-business-expenses`.
- If the question is about billable time or project delivery, compose with `odoo-business-timesheet-project-services`.
- If finance posting dominates, compose with `odoo-business-accounting`.

# Compose with sibling skills
- `odoo-business-timesheet-project-services`
- `odoo-business-expenses`
- `odoo-business-accounting`

# References
`references/overview.md` (scope + anchors) · `references/checklist.md` · `references/examples.md`
