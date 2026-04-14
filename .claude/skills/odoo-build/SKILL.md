---
name: odoo-build
description: "Implement Odoo changes in Python, XML, security, manifest, and controller files. Use only when the user wants code or configuration changes produced, not when they still need planning or comparison."
---

# Purpose
Create or modify Odoo code, XML, manifests, security files, and migration stubs according to approved scope and existing conventions.

# Primary routing rule
Use this skill only when the primary requested output is changed code or config artifacts. If the user is still deciding approach, use `odoo-plan`.

# Use this skill when
- implement an Odoo feature or bug fix
- add or change models, views, actions, controllers, or manifests
- create access files, data files, or migration stubs
- apply an already-decided implementation approach

# Do not use this skill when
- the primary requested output is still a plan or option comparison
- the request is purely business-process explanation
- the task is release orchestration, review, or retrospective only

# Required inputs
- user request and desired output artifact
- target module(s), files, or flow if known
- current diff, traceback, failing scenario, or release context when available

# Workflow
1. Confirm the requested output artifact belongs in this skill; redirect if it does not.
2. Map the request to the smallest relevant Odoo modules, docs, and source anchors.
3. Apply the deterministic checks in `references/checklist.md`.
4. Produce the artifact described below, naming assumptions, blockers, and cross-app effects.
5. Hand off or compose with sibling skills when the request crosses this skill boundary.

# Output contract
- code changes
- changed file list
- assumptions or follow-up validation needs

# Guardrails
- Stay inside this sprint-phase responsibility; do not absorb neighboring tasks.
- Prefer Odoo <ODOO_MAJOR_VERSION> docs for functional rules and Odoo CE <ODOO_MAJOR_VERSION> source for implementation truth.
- Call out docs or source mismatches instead of hiding them.
- Name permissions impact, migration impact, and cross-app modules whenever relevant.
- Name rollback or staging risk whenever release or data impact exists.

# Must hand off when
- If scope or approach is still undecided, hand off to `odoo-plan`.
- If the user asks for findings on an existing diff, hand off to `odoo-review`.
- Compose with technical specialists whenever implementation crosses ORM, UI, security, migration, or performance boundaries.

# Compose with sibling skills
- `odoo-orm-modeling`
- `odoo-view-ui`
- `odoo-security`

# References
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
