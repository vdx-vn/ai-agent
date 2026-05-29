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
Question or artifact, module/entrypoint if known, surrounding context when available.

# Workflow
Confirm → Read anchors → Apply checklist → Answer with guidance → State boundary decision.

# Output contract
- base website or ecommerce flow
- cross-app impacts
- roles and decision points
- golden-path test ideas
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only this skill's domain. Anchor to Odoo docs + CE source, not generic ERP intuition.
- Highlight cross-app, accounting, or security effects. Redirect to task skills for planning/building/testing/shipping.
- Keep public or portal customer journey here. Keep template, xpath, and other UI mechanics with `odoo-view-ui` unless they directly change process meaning.

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
`references/overview.md` (scope + anchors) · `references/checklist.md` · `references/examples.md`
