---
name: odoo-business-timesheet-project-services
description: "Explain Odoo services delivery across project, task, timesheet, planning, helpdesk, and sales invoicing links. Use when the primary entrypoint is service work, project tasks, or billable time."
---

# Purpose
Explain Odoo service-delivery flows across project, task, timesheet, planning, helpdesk, and sales invoicing links.

# Primary routing rule
Use this skill only when the primary business entrypoint is project, task, timesheet, helpdesk, planning, or service delivery.

# Use this skill when
- explain project, task, or timesheet process impact
- trace service delivery into invoicing
- map planning or helpdesk links to billable work

# Do not use this skill when
- the primary entrypoint is HR contract or payroll policy
- the request is pure expense reimbursement
- the issue is technical ORM or ACL design

# Required inputs
Question or artifact, module/entrypoint if known, surrounding context when available.

# Workflow
Confirm → Read anchors → Apply checklist → Answer with guidance → State boundary decision.

# Output contract
- base service flow
- cross-app impacts
- roles and decision points
- golden-path test ideas
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only this skill's domain. Anchor to Odoo docs + CE source, not generic ERP intuition.
- Highlight cross-app, accounting, or security effects. Redirect to task skills for planning/building/testing/shipping.

# Must hand off when
- If workforce policy or payroll prerequisites dominate, compose with `odoo-business-hr`.
- If the main issue is finance posting, compose with `odoo-business-accounting`.
- If the primary entrypoint is backend quote or order rather than service delivery, compose with `odoo-business-sales`.

# Compose with sibling skills
- `odoo-business-sales`
- `odoo-business-hr`
- `odoo-business-accounting`

# References
`references/overview.md` (scope + anchors) · `references/checklist.md` · `references/examples.md`
