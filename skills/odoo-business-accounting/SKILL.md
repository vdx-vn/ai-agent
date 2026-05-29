---
name: odoo-business-accounting
description: "Explain Odoo accounting flow across invoices, bills, journals, taxes, payments, reconciliation, localization, and valuation crossovers. Use when the primary entrypoint is a finance document, posting event, tax rule, or valuation impact."
---

# Purpose
Explain Odoo accounting flow and finance implications across invoices, bills, journals, taxes, payments, reconciliation, localization, and valuation.

# Primary routing rule
Use this skill only when the primary business entrypoint is invoice, bill, payment, tax, reconciliation, localization, or valuation impact.

# Use this skill when
- explain invoice, bill, payment, tax, or reconciliation impact
- trace valuation or business workflow changes into accounting
- reason about localization or fiscal-position behavior

# Do not use this skill when
- the task is only sales or purchase process without finance focus
- the issue is generic access rights
- the question is pure technical ORM design

# Required inputs
Question or artifact, module/entrypoint if known, surrounding context when available.

# Workflow
Confirm → Read anchors → Apply checklist → Answer with guidance → State boundary decision.

# Output contract
- base accounting flow
- cross-app impacts
- roles and decision points
- golden-path test ideas
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only this skill's domain. Anchor to Odoo docs + CE source, not generic ERP intuition.
- Highlight cross-app, accounting, or security effects. Redirect to task skills for planning/building/testing/shipping.

# Must hand off when
- If the question begins from backend quoting or ordering, compose with `odoo-business-sales`.
- If it begins from expenses or HR approvals, compose with `odoo-business-expenses` or `odoo-business-hr`.
- If the primary ask is addon placement, hand off to `odoo-architecture`.

# Compose with sibling skills
- `odoo-business-sales`
- `odoo-business-purchase`
- `odoo-business-inventory`
- `odoo-business-expenses`
- `odoo-business-hr`
- `odoo-architecture`

# References
`references/overview.md` (scope + anchors) · `references/checklist.md` · `references/examples.md`
