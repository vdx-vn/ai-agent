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
- user question or design decision
- current module, entrypoint, or artifact under discussion if known
- surrounding business or technical context when available

# Workflow
1. Confirm the requested decision or process belongs in this skill; redirect if it does not.
2. Read only the smallest relevant anchors from `references/overview.md`.
3. Apply the rule or process checklist in `references/checklist.md`.
4. Answer with Odoo-specific guidance, tradeoffs, downstream effects, and boundary notes.
5. State a boundary decision with primary skill, composed siblings, and deferred scope.

# Output contract
- base warehouse or stock flow
- cross-app impacts
- roles and decision points
- golden-path test ideas
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only the domain or technical question this skill owns.
- Use Odoo <ODOO_MAJOR_VERSION> docs as guidance and Odoo CE <ODOO_MAJOR_VERSION> source as runtime truth.
- Do not answer from generic ERP intuition; anchor to Odoo <ODOO_MAJOR_VERSION> terms, addons, and bridge modules.
- Highlight cross-app, accounting, or security effects when they materially change the answer.
- Redirect to task skills when the user needs planning, building, testing, or shipping.

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
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
