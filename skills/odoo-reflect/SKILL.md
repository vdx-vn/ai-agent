---
name: odoo-reflect
description: "Reflect on completed Odoo work. Use when the primary output is a retrospective with lessons learned, missed assumptions, and concrete follow-up actions after review, testing, or release."
---

# Purpose
Produce a retrospective for completed Odoo work, covering what happened, what was missed, and what follow-up actions remain.

# Primary routing rule
Use this skill only when the primary requested output is a retrospective or lessons learned artifact after work already happened.

# Use this skill when
- run a retrospective after review, testing, or release
- summarize lessons learned from an Odoo change
- identify follow-up hardening or debt after completion
- turn observed misses into concrete future actions

# Do not use this skill when
- the task is still active planning or implementation
- the request is live code review
- the task is test execution

# Required inputs
Artifact + target module/files if known + diff/traceback/context when available.

# Workflow
Confirm → Map to Odoo modules/anchors → Apply checklist → Produce artifact → State boundary decision.

# Output contract
- summary of what happened
- gaps or misses
- lessons learned
- follow-up tasks
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Stay in sprint-phase scope; do not absorb neighbors.
- Anchor to Odoo docs (functional rules) and CE source (implementation truth); call out mismatches.
- Name permissions, migration, cross-app, and rollback risks when relevant.
- Produce concrete lessons and follow-up actions, not vague commentary.

# Must hand off when
- If the user is still deciding what to build, hand off to `odoo-think` or `odoo-plan`.
- If the user wants findings on a current diff, hand off to `odoo-review`.
- Compose with business skills when the lesson depends on domain process misunderstanding.

# Compose with sibling skills
- `odoo-think`
- `odoo-plan`
- `odoo-review`
- `odoo-test`

# References
`references/overview.md` (scope + anchors) · `references/checklist.md` · `references/examples.md`
