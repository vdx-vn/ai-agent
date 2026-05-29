---
name: odoo-ship
description: "Prepare Odoo changes for staging or release. Use when the primary output is go or no-go readiness, rollout sequencing, staging checks, rollback considerations, and production-facing cautions, not low-level command semantics."
---

# Purpose
Prepare release readiness for Odoo changes, including go or no-go criteria, staging checks, rollout sequencing, rollback considerations, and production-facing cautions.

# Primary routing rule
Use this skill only when the user wants release readiness or rollout sequencing. If the user needs CLI flag semantics or environment mechanics, hand off to `odoo-delivery-ops`. If the primary issue is data or schema evolution, compose with `odoo-upgrade-migration`.

# Use this skill when
- prepare staging or production release
- build deployment or rollout checklist
- decide whether current work is ready to ship
- identify rollback, migration, or production risk before release

# Do not use this skill when
- the primary requested output is low-level CLI or runtime semantics
- the task is still design or implementation
- the task is retrospective only

# Required inputs
Artifact + target module/files if known + diff/traceback/context when available.

# Workflow
Confirm → Map to Odoo modules/anchors → Apply checklist → Produce artifact → State boundary decision.

# Output contract
- evidence status: executed, planned, or blocked
- go or no-go readiness summary
- ship checklist and rollout sequence
- staging verification list
- rollback or production cautions
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Stay in sprint-phase scope; do not absorb neighbors.
- Anchor to Odoo docs (functional rules) and CE source (implementation truth); call out mismatches.
- Name permissions, migration, cross-app, and rollback risks when relevant.
- Do not call a change ready if critical validation or migration evidence is still missing.

# Must hand off when
- If the user asks what `-u`, `-i`, `--reinit`, workers, or Odoo.sh stages do, hand off to `odoo-delivery-ops`.
- If schema or data migration strategy is central, compose with `odoo-upgrade-migration`.
- If validation evidence is still missing, compose with `odoo-test` before calling the change ready.

# Compose with sibling skills
- `odoo-delivery-ops`
- `odoo-upgrade-migration`
- `odoo-test`

# References
`references/overview.md` (scope + anchors) · `references/checklist.md` · `references/examples.md`
