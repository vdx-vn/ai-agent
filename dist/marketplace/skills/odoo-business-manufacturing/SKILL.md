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
- base manufacturing flow
- cross-app impacts
- roles and decision points
- golden-path test ideas
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only the domain or technical question this skill owns.
- Use current Odoo docs as guidance and current Odoo CE source as runtime truth.
- Do not answer from generic ERP intuition; anchor to current Odoo terms, addons, and bridge modules.
- Highlight cross-app, accounting, or security effects when they materially change the answer.
- Redirect to task skills when the user needs planning, building, testing, or shipping.

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
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
