---
name: odoo-business-manufacturing
description: "Explain Odoo manufacturing processes including BoM, MO, operations, work centers, component and finished moves, and MRP cross-app behavior. Use when the primary entrypoint is BoM, MO, work center, routing, or subcontracting."
---

# Purpose
Explain Odoo manufacturing process and its cross-app behavior across stock, procurement, sales, and accounting.

# Primary routing rule
Use this skill only when the primary business entrypoint is BoM, MO, work center, routing, subcontracting, or production planning. If the entrypoint is warehouse documents or routes without production-control logic, use `odoo-business-inventory`.

# Use this skill when
- explain BoM, MO, routing, work-center, or production impact
- reason about manufacturing links to stock, purchase, or sales
- trace component and finished-move behavior from a production entrypoint

# Do not use this skill when
- the primary entrypoint is a warehouse document or route with no production control decision
- the question is accounting-only without production context
- the issue is technical ACL or ORM design

# Required inputs
Question or artifact, module/entrypoint if known, surrounding context when available.

# Workflow
Confirm → Read anchors → Apply checklist → Answer with guidance → State boundary decision.

# Output contract
- base manufacturing flow
- cross-app impacts
- roles and decision points
- golden-path test ideas
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only this skill's domain. Anchor to Odoo docs + CE source, not generic ERP intuition.
- Highlight cross-app, accounting, or security effects. Redirect to task skills for planning/building/testing/shipping.

# Must hand off when
- If the question starts from receipts, deliveries, transfers, or route design, hand off to `odoo-business-inventory`.
- If purchasing of components dominates, compose with `odoo-business-purchase`.
- If finance posting dominates, compose with `odoo-business-accounting`.

# Compose with sibling skills
- `odoo-business-inventory`
- `odoo-business-purchase`
- `odoo-business-sales`
- `odoo-business-accounting`

# References
`references/overview.md` (scope + anchors) · `references/checklist.md` · `references/examples.md`
