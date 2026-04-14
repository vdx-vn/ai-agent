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
- user question or design decision
- current module, entrypoint, or artifact under discussion if known
- surrounding business or technical context when available

# Workflow
1. Confirm the requested decision or process belongs in this skill; redirect if it does not.
2. Read only the smallest relevant anchors from `references/overview.md`.
3. Apply the rule or process checklist in `references/checklist.md`.
4. Answer with Odoo-specific guidance, tradeoffs, downstream effects, and boundary notes.
5. Point to sibling skills when implementation workflow or adjacent domains matter.

# Output contract
- base purchase flow
- cross-app impacts
- roles and decision points
- golden-path test ideas

# Guardrails
- Answer only the domain or technical question this skill owns.
- Use Odoo <ODOO_MAJOR_VERSION> docs as guidance and Odoo CE <ODOO_MAJOR_VERSION> source as runtime truth.
- Do not answer from generic ERP intuition; anchor to Odoo <ODOO_MAJOR_VERSION> terms, addons, and bridge modules.
- Highlight cross-app, accounting, or security effects when they materially change the answer.
- Redirect to task skills when the user needs planning, building, testing, or shipping.

# Must hand off when
- If the question starts from warehouse routes or pickings without buyer intent, compose with `odoo-business-inventory`.
- If the main driver is BoM or MO logic, compose with `odoo-business-manufacturing`.
- If finance posting dominates, compose with `odoo-business-accounting`.

# Compose with sibling skills
- `odoo-business-inventory`
- `odoo-business-accounting`
- `odoo-business-manufacturing`

# References
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
