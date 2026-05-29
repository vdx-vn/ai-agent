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
Question or artifact, module/entrypoint if known, surrounding context when available.

# Workflow
Confirm → Read anchors → Apply checklist → Answer with guidance → State boundary decision.

# Output contract
- base backend sales flow
- cross-app impacts
- roles and decision points
- golden-path test ideas
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only this skill's domain. Anchor to Odoo docs + CE source, not generic ERP intuition.
- Highlight cross-app, accounting, or security effects. Redirect to task skills for planning/building/testing/shipping.

# Must hand off when
- If the entrypoint is website, cart, checkout, portal, or public form, hand off to `odoo-business-website-ecommerce`.
- If the question is mainly stock routes or pickings, compose with `odoo-business-inventory`.
- If finance posting or taxes dominate, compose with `odoo-business-accounting`.

# Compose with sibling skills
- `odoo-business-inventory`
- `odoo-business-accounting`
- `odoo-business-website-ecommerce`

# References
`references/overview.md` (scope + anchors) · `references/checklist.md` · `references/examples.md`
