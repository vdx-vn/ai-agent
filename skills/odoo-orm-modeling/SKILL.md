---
name: odoo-orm-modeling
description: "Guide Odoo model and field design, compute, onchange, constrains, API semantics, and recordset-safe ORM patterns. Use when the primary output is a model or ORM design decision, not UI mechanics or business-flow explanation."
---

# Purpose
Guide model, field, API, recordset, and compute or onchange design in Odoo ORM.

# Primary routing rule
Use this skill only when the primary requested output is a model or ORM design decision.

# Use this skill when
- design a model or field
- choose compute, store, inverse, onchange, or constrains behavior
- review ORM patterns and recordset usage

# Do not use this skill when
- the primary requested output is view or UI design
- the task is a business-process walkthrough
- the issue is mainly permissions or controller auth

# Required inputs
Question or artifact, module/entrypoint if known, surrounding context when available.

# Workflow
Confirm → Read anchors → Apply checklist → Answer with guidance → State boundary decision.

# Output contract
- field or method pattern recommendation
- ORM anti-pattern warnings
- recordset or decorator guidance
- follow-up test notes
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only this skill's domain. Anchor to Odoo docs + CE source, not generic ERP intuition.
- Highlight cross-app, accounting, or security effects. Redirect to task skills for planning/building/testing/shipping.

# Must hand off when
- If the user asks how this should appear in views or menus, hand off to `odoo-view-ui`.
- If the issue is mainly performance under load, compose with `odoo-performance`.
- If access or trust boundaries dominate, compose with `odoo-security`.

# Compose with sibling skills
- `odoo-build`
- `odoo-view-ui`
- `odoo-performance`
- `odoo-security`
- `odoo-orm-modeling`

# References
`references/overview.md` (scope + anchors) · `references/checklist.md` · `references/examples.md`
