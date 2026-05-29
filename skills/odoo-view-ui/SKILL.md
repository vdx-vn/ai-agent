---
name: odoo-view-ui
description: "Guide Odoo views, actions, menus, QWeb, backend UI, website template mechanics, and OWL or web-client changes. Use when the primary question is UI structure, template behavior, xpath strategy, or action behavior, not business process or ORM semantics."
---

# Purpose
Guide Odoo views, actions, menus, QWeb, website template mechanics, backend UI, and OWL or web-client UI changes.

# Primary routing rule
Use this skill only when the primary requested output is a view, action, menu, template, xpath, OWL, or client-side UI decision. Even on website pages, keep this skill primary when the user asks about template or UI mechanics.

# Use this skill when
- change form, tree, kanban, search, or QWeb views
- add or adjust actions and menus
- touch OWL or web-client UI behavior
- decide website template, xpath, or action mechanics

# Do not use this skill when
- the primary requested output is ORM semantics
- the request is about access policy
- the task is a business-process map

# Required inputs
Question or artifact, module/entrypoint if known, surrounding context when available.

# Workflow
Confirm → Read anchors → Apply checklist → Answer with guidance → State boundary decision.

# Output contract
- view strategy
- action and menu notes
- inheritance or xpath cautions
- UI-specific follow-up tests
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only this skill's domain. Anchor to Odoo docs + CE source, not generic ERP intuition.
- Highlight cross-app, accounting, or security effects. Redirect to task skills for planning/building/testing/shipping.
- Keep customer journey or checkout process meaning with `odoo-business-website-ecommerce`; keep template, xpath, and action mechanics here.

# Must hand off when
- If the UI question starts from website cart, checkout, portal, or public form entrypoints but the user mainly wants process meaning, compose with `odoo-business-website-ecommerce`.
- If model semantics dominate, hand off to `odoo-orm-modeling`.
- If addon placement dominates, hand off to `odoo-architecture`.

# Compose with sibling skills
- `odoo-build`
- `odoo-business-website-ecommerce`
- `odoo-architecture`
- `odoo-orm-modeling`

# References
`references/overview.md` (scope + anchors) · `references/checklist.md` · `references/examples.md`
