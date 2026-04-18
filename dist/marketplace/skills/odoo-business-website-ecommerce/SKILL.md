---
name: odoo-business-website-ecommerce
description: "Explain Odoo website and ecommerce flow across public pages, public forms, portal, shop, cart, checkout, online sales, stock visibility, and CRM capture. Use when the primary entrypoint is a public or portal customer journey, not backend sales workflow or website template mechanics."
---

# Purpose
Explain Odoo website and ecommerce flow across content, forms, cart, checkout, online sales, stock visibility, and CRM capture.

# Primary routing rule
Use this skill only when the primary entrypoint is a public page, public form, portal, cart, checkout, or online storefront behavior. If the user asks about template, xpath, QWeb, OWL, or action mechanics, use `odoo-view-ui`. If the entrypoint is lead, quotation, salesperson action, or backend sales order, use `odoo-business-sales`.

# Use this skill when
- explain website or ecommerce process impact
- trace cart to order to delivery flow
- reason about website forms, stock visibility, portal, or lead capture
- explain public or portal customer journey behavior

# Do not use this skill when
- the primary entrypoint is backend quote or sales order workflow
- the task is backend form or list view design only
- the main ask is template or xpath mechanics
- the issue is mainly ACL or ORM design

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
- base website or ecommerce flow
- cross-app impacts
- roles and decision points
- golden-path test ideas
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only the domain or technical question this skill owns.
- Use current Odoo docs as guidance and current Odoo CE source as runtime truth.
- Do not answer from generic ERP intuition; anchor to current Odoo terms, addons, and bridge modules.
- Highlight cross-app, accounting, or security effects when they materially change the answer.
- Keep public or portal customer journey here. Keep template, xpath, and other UI mechanics with `odoo-view-ui` unless they directly change process meaning.
- Redirect to task skills when the user needs planning, building, testing, or shipping.

# Must hand off when
- If the primary entrypoint is opportunity, quotation, salesperson action, or backend sales order, hand off to `odoo-business-sales`.
- If the main question is backend or website UI structure, compose with `odoo-view-ui`.
- If exposure or portal permissions dominate, compose with `odoo-security`.

# Compose with sibling skills
- `odoo-business-sales`
- `odoo-business-inventory`
- `odoo-view-ui`
- `odoo-security`

# References
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
