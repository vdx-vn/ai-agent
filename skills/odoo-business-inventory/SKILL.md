---
name: odoo-business-inventory
description: "Explain Odoo inventory and warehouse operations, including receipts, deliveries, transfers, routes, replenishment, lots, serials, and valuation touchpoints. Use when the primary entrypoint is a stock document, route, or warehouse operation and not a manufacturing-control decision."
---

# Purpose
Explain Odoo warehouse and stock flows, including routes, replenishment, movement documents, traceability, and valuation touchpoints.

# Primary routing rule
Use this skill only when the primary business entrypoint is receipt, delivery, transfer, route, replenishment, or stock move. If the entrypoint is BoM, MO, work center, routing, or subcontracting, use `odoo-business-manufacturing`.

# Use this skill when
- explain warehouse or stock-process impact
- reason about routes, replenishment, pickings, lots, or serials
- trace inventory changes into sales, purchase, MRP, or accounting

# Do not use this skill when
- the primary entrypoint is BoM, MO, work center, or routing
- the issue is only accounting reporting
- the question is mainly security or ORM design

# Required inputs
Question or artifact, module/entrypoint if known, surrounding context when available.

# Workflow
Confirm → Read anchors → Apply checklist → Answer with guidance → State boundary decision.

# Output contract
- base warehouse or stock flow
- cross-app impacts
- roles and decision points
- golden-path test ideas
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only this skill's domain. Anchor to Odoo docs + CE source, not generic ERP intuition.
- Highlight cross-app, accounting, or security effects. Redirect to task skills for planning/building/testing/shipping.

# Must hand off when
- If the primary entrypoint is MO, BoM, or work center, hand off to `odoo-business-manufacturing`.
- If the question starts from backend order flow, compose with `odoo-business-sales` or `odoo-business-purchase`.
- If finance posting dominates, compose with `odoo-business-accounting`.

# Compose with sibling skills
- `odoo-business-sales`
- `odoo-business-purchase`
- `odoo-business-accounting`
- `odoo-business-manufacturing`

# References
`references/overview.md` (scope + anchors) · `references/checklist.md` · `references/examples.md`
