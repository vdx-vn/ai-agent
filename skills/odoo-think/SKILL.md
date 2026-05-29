---
name: odoo-think
description: "Diagnose Odoo request scope before planning. Use when the primary output is a scoping brief with impacted modules, business entrypoints, risks, unknowns, and decision framing. Do not use for implementation steps or code changes."
---

# Purpose
Frame the request, identify impacted modules, business entrypoints, risks, and unknowns before any execution plan or implementation begins.

# Primary routing rule
Use this skill only when the primary requested output is a scoping brief or impact diagnosis. If the user wants ordered steps, file-by-file actions, or acceptance criteria, hand off to `odoo-plan`.

# Use this skill when
- scope a request before planning
- identify affected modules, bridge addons, or business entrypoints
- surface major technical, security, accounting, inventory, payroll, or upgrade risks
- clarify unknowns that block a safe plan

# Do not use this skill when
- the primary requested output is an execution plan
- the user is asking to implement or patch code now
- the task is review, testing, shipping, or retrospective work

# Required inputs
Artifact + target module/files if known + diff/traceback/context when available.

# Workflow
Confirm → Map to Odoo modules/anchors → Apply checklist → Produce artifact → State boundary decision.

# Output contract
- problem statement
- impacted modules and bridge addons
- affected business flow and entrypoint
- top risks and unknowns
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Stay in sprint-phase scope; do not absorb neighbors.
- Anchor to Odoo docs (functional rules) and CE source (implementation truth); call out mismatches.
- Name permissions, migration, cross-app, and rollback risks when relevant.
- Do not drift into ordered implementation steps or code changes.

# Must hand off when
- If the user asks for ordered implementation steps, files, or acceptance criteria, hand off to `odoo-plan`.
- If the user asks for concrete code changes, hand off to `odoo-build`.
- If the question is mainly business-process meaning, compose with the matching business skill.

# Compose with sibling skills
- `odoo-plan`
- `odoo-build`
- `odoo-architecture`

# References
`references/overview.md` (scope + anchors) · `references/checklist.md` · `references/examples.md`
