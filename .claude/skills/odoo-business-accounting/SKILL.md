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
- base accounting flow
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
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
