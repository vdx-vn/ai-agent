---
name: odoo-view-ui
description: "Guide Odoo views, actions, menus, QWeb, backend UI, and OWL or web-client changes. Use when the primary question is UI structure or view behavior, not business process or ORM semantics."
---

# Purpose
Guide Odoo views, actions, menus, QWeb, backend UI, and OWL or web-client UI changes.

# Primary routing rule
Use this skill only when the primary requested output is a view, action, menu, template, or client-side UI decision.

# Use this skill when
- change form, tree, kanban, search, or QWeb views
- add or adjust actions and menus
- touch OWL or web-client UI behavior

# Do not use this skill when
- the primary requested output is ORM semantics
- the request is about access policy
- the task is a business-process map

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
- view strategy
- action and menu notes
- inheritance or xpath cautions
- UI-specific follow-up tests

# Guardrails
- Answer only the domain or technical question this skill owns.
- Use Odoo <ODOO_MAJOR_VERSION> docs as guidance and Odoo CE <ODOO_MAJOR_VERSION> source as runtime truth.
- Do not answer from generic ERP intuition; anchor to Odoo <ODOO_MAJOR_VERSION> terms, addons, and bridge modules.
- Highlight cross-app, accounting, or security effects when they materially change the answer.
- Redirect to task skills when the user needs planning, building, testing, or shipping.

# Must hand off when
- If the UI question starts from website cart, checkout, portal, or public form entrypoints, compose with `odoo-business-website-ecommerce`.
- If model semantics dominate, hand off to `odoo-orm-modeling`.
- If addon placement dominates, hand off to `odoo-architecture`.

# Compose with sibling skills
- `odoo-build`
- `odoo-business-website-ecommerce`
- `odoo-architecture`

# References
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
