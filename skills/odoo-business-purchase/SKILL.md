---
name: odoo-business-purchase
description: "Explain Odoo purchase lifecycle from RFQ and PO through receipt and vendor billing. Use when the primary business entrypoint is buying, procurement, or replenishment through purchasing."
---

# Purpose
Explain Odoo purchase lifecycle from RFQ and purchase order through receipt, replenishment, and vendor billing.

# Primary routing rule
Use this skill only when the primary business entrypoint is RFQ, purchase order, replenishment through buying, or vendor-side procurement.

# Use this skill when
- explain purchase workflow impact
- trace RFQ or PO to receipt and vendor bill
- reason about replenishment or procurement from a purchase entrypoint

# Do not use this skill when
- the primary process is sales, manufacturing control, or internal warehouse operation
- the question is accounting-only without purchase entrypoint
- the issue is technical security or ORM design

# Required inputs
Question or artifact, module/entrypoint if known, surrounding context when available.

# Workflow
Confirm → Read anchors → Apply checklist → Answer with guidance → State boundary decision.

# Output contract
- base purchase flow
- cross-app impacts
- roles and decision points
- golden-path test ideas
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only this skill's domain. Anchor to Odoo docs + CE source, not generic ERP intuition.
- Highlight cross-app, accounting, or security effects. Redirect to task skills for planning/building/testing/shipping.

# Must hand off when
- If the question starts from warehouse routes or pickings without buyer intent, compose with `odoo-business-inventory`.
- If the main driver is BoM or MO logic, compose with `odoo-business-manufacturing`.
- If finance posting dominates, compose with `odoo-business-accounting`.

# Compose with sibling skills
- `odoo-business-inventory`
- `odoo-business-accounting`
- `odoo-business-manufacturing`

# References
`references/overview.md` (scope + anchors) · `references/checklist.md` · `references/examples.md`
