---
name: odoo-business-sales
description: "Explain Odoo backend sales lifecycle from lead or opportunity and quotation through order, delivery, and invoicing. Use when the primary business entrypoint is CRM, quotation, or backend sales order, not website cart or checkout."
---

# Purpose
Explain Odoo backend sales lifecycle and the cross-app links from CRM through quotation, order, delivery, and invoicing.

# Primary routing rule
Use this skill only when the primary business entrypoint is lead, opportunity, quotation, salesperson action, or backend sales order. If the entrypoint is page, form, cart, checkout, or portal, use `odoo-business-website-ecommerce`.

# Use this skill when
- explain sales workflow impact from CRM or backend sales entrypoints
- trace quotation to order to delivery and invoice
- reason about CRM, delivery, or invoicing links from a salesperson or backend order flow

# Do not use this skill when
- the primary entrypoint is website cart, checkout, portal, or public form
- the task is mainly purchase-side process
- the issue is purely technical ORM or ACL design

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
- base backend sales flow
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
- If the entrypoint is website, cart, checkout, portal, or public form, hand off to `odoo-business-website-ecommerce`.
- If the question is mainly stock routes or pickings, compose with `odoo-business-inventory`.
- If finance posting or taxes dominate, compose with `odoo-business-accounting`.

# Compose with sibling skills
- `odoo-business-inventory`
- `odoo-business-accounting`
- `odoo-business-website-ecommerce`

# References
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
