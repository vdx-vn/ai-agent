---
name: odoo-build
description: "Implement Odoo changes in Python, XML, security, manifest, and controller files. Use when the primary output is changed code or configuration artifacts, not when the user still needs planning or comparison."
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
Artifact + target module/files if known + diff/traceback/context when available.

# Workflow
Confirm → Map to Odoo modules/anchors → Apply checklist → Produce artifact → State boundary decision.

# Output contract
- code changes
- changed file list
- follow-up validation needs
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Stay in sprint-phase scope; do not absorb neighbors.
- Anchor to Odoo docs (functional rules) and CE source (implementation truth); call out mismatches.
- Name permissions, migration, cross-app, and rollback risks when relevant.
- Avoid speculative abstractions and keep changes inside approved scope.

# Must hand off when
- If scope or approach is still undecided, hand off to `odoo-plan`.
- If the user asks for findings on an existing diff, hand off to `odoo-review`.
- If migration strategy dominates the request, compose with `odoo-upgrade-migration`.
- Compose with technical specialists whenever implementation crosses ORM, UI, security, migration, or performance boundaries.

# Compose with sibling skills
- `odoo-plan`
- `odoo-review`
- `odoo-orm-modeling`
- `odoo-view-ui`
- `odoo-security`
- `odoo-upgrade-migration`

# References
`references/overview.md` (scope + anchors) · `references/checklist.md` · `references/examples.md`
