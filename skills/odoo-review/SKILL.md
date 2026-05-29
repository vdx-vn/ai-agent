---
name: odoo-review
description: "Review existing Odoo changes before merge. Use when the primary output is review findings on a diff, patch, or implementation artifact about architecture fit, maintainability, correctness, and broad risk. Do not use when the main ask is to execute validation."
---

# Purpose
Review an existing Odoo change artifact for architecture fit, maintainability, correctness, broad risk, and cross-app impact before merge.

# Primary routing rule
Use this skill only when the primary requested output is review findings on an existing artifact. If the user wants executed validation evidence, use `odoo-test`. If the prompt centers on exposure or trust boundaries, compose with or defer to `odoo-security`.

# Use this skill when
- review a diff or patch before merge
- check architecture fit, maintainability, and broad risk
- find issues in an implemented change artifact
- perform pre-merge structural review

# Do not use this skill when
- the primary requested output is executed validation or regression evidence
- no diff, patch, or implemented artifact exists yet
- the task is a retrospective after completion

# Required inputs
Artifact + target module/files if known + diff/traceback/context when available.

# Workflow
Confirm → Map to Odoo modules/anchors → Apply checklist → Produce artifact → State boundary decision.

# Output contract
- evidence status: reasoned review only
- findings by severity
- required fixes
- suggested improvements
- untested risk areas
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Stay in sprint-phase scope; do not absorb neighbors.
- Anchor to Odoo docs (functional rules) and CE source (implementation truth); call out mismatches.
- Name permissions, migration, cross-app, and rollback risks when relevant.
- Do not imply commands were run or validation evidence exists unless execution evidence is provided separately.

# Must hand off when
- If there is no artifact yet, hand off to `odoo-think` or `odoo-plan`.
- If the user asks to run validation or produce execution evidence, hand off to `odoo-test`.
- If permissions, exposure, or trust boundaries are central, compose with `odoo-security`.

# Compose with sibling skills
- `odoo-think`
- `odoo-plan`
- `odoo-security`
- `odoo-test`
- `odoo-testing-reference`

# References
`references/overview.md` (scope + anchors) · `references/checklist.md` · `references/examples.md`
