---
name: odoo-plan
description: "Turn Odoo requests into execution plans. Use when the primary output is an ordered plan with file and module mapping, acceptance criteria, test strategy, rollout notes, and open decisions. Do not use for code changes."
---

# Purpose
Convert an Odoo request into an execution plan with files, modules, acceptance criteria, validation, rollout notes, and unresolved decisions.

# Primary routing rule
Use this skill only when the user wants a plan artifact. If the user wants a risk brief, use `odoo-think`. If the user wants code edits, use `odoo-build`.

# Use this skill when
- build a step-by-step implementation plan
- identify files, modules, tests, and rollout notes before coding
- define acceptance criteria and unresolved design decisions
- turn scoped work into an actionable execution sequence

# Do not use this skill when
- the primary requested output is only impact analysis or risk discovery
- the user wants direct implementation or patch generation
- the task is a retrospective or release go or no-go call

# Required inputs
Artifact + target module/files if known + diff/traceback/context when available.

# Workflow
Confirm → Map to Odoo modules/anchors → Apply checklist → Produce artifact → State boundary decision.

# Output contract
- ordered implementation steps
- target files and modules
- acceptance criteria and open decisions
- test matrix and rollout notes
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Stay in sprint-phase scope; do not absorb neighbors.
- Anchor to Odoo docs (functional rules) and CE source (implementation truth); call out mismatches.
- Name permissions, migration, cross-app, and rollback risks when relevant.
- Keep this skill at planning depth; do not drift into code generation.

# Must hand off when
- If the user asks for code, XML, manifest, or security changes now, hand off to `odoo-build`.
- If migration strategy becomes central, compose with `odoo-upgrade-migration`.
- If the scope is still unclear, step back to `odoo-think`.

# Compose with sibling skills
- `odoo-think`
- `odoo-build`
- `odoo-test`
- `odoo-upgrade-migration`

# References
`references/overview.md` (scope + anchors) · `references/checklist.md` · `references/examples.md`
