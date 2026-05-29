---
name: odoo-business-expenses
description: "Explain Odoo expense submission, approval, posting, and reimbursement flow together with HR and accounting links. Use when the primary entrypoint is expense claim, expense sheet, reimbursement, or posting, even if HR actors are involved."
---

# Purpose
Explain Odoo expense flow from submission through approval, posting, and reimbursement, including HR and accounting links.

# Primary routing rule
Use this skill only when the primary business entrypoint is expense claim, expense sheet, reimbursement, or expense posting. If the entrypoint is employee contract, attendance, time off, or payroll prerequisite, use `odoo-business-hr`.

# Use this skill when
- explain expense-sheet process impact
- trace expense approval into accounting
- reason about employee-paid or company-paid reimbursement behavior

# Do not use this skill when
- the primary entrypoint is employee master data or payroll prerequisite
- the task is generic AP or vendor-bill flow
- the issue is pure technical field design

# Required inputs
Question or artifact, module/entrypoint if known, surrounding context when available.

# Workflow
Confirm → Read anchors → Apply checklist → Answer with guidance → State boundary decision.

# Output contract
- base expense flow
- cross-app impacts
- roles and decision points
- golden-path test ideas
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only this skill's domain. Anchor to Odoo docs + CE source, not generic ERP intuition.
- Highlight cross-app, accounting, or security effects. Redirect to task skills for planning/building/testing/shipping.

# Must hand off when
- If the question is mainly about employee contract, attendance, or payroll prerequisites, hand off to `odoo-business-hr`.
- If finance posting dominates after approval, compose with `odoo-business-accounting`.
- If permissions or exposure dominate, compose with `odoo-security`.

# Compose with sibling skills
- `odoo-business-hr`
- `odoo-business-accounting`
- `odoo-security`

# References
`references/overview.md` (scope + anchors) · `references/checklist.md` · `references/examples.md`
