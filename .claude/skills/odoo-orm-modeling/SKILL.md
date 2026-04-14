---
name: odoo-orm-modeling
description: "Guide Odoo model and field design, compute, onchange, constrains, API semantics, and recordset-safe ORM patterns. Use when the primary question is model behavior or ORM implementation pattern."
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
- field or method pattern recommendation
- ORM anti-pattern warnings
- recordset or decorator guidance
- follow-up test notes

# Guardrails
- Answer only the domain or technical question this skill owns.
- Use Odoo <ODOO_MAJOR_VERSION> docs as guidance and Odoo CE <ODOO_MAJOR_VERSION> source as runtime truth.
- Do not answer from generic ERP intuition; anchor to Odoo <ODOO_MAJOR_VERSION> terms, addons, and bridge modules.
- Highlight cross-app, accounting, or security effects when they materially change the answer.
- Redirect to task skills when the user needs planning, building, testing, or shipping.

# Must hand off when
- If the user asks how this should appear in views or menus, hand off to `odoo-view-ui`.
- If the issue is mainly performance under load, compose with `odoo-performance`.
- If access or trust boundaries dominate, compose with `odoo-security`.

# Compose with sibling skills
- `odoo-build`
- `odoo-performance`
- `odoo-security`

# References
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
