---
name: odoo-upgrade-migration
description: "Guide Odoo schema, data, and module upgrades, migration scripts, custom DB upgrade steps, and noupdate handling. Use when the primary question is how to preserve and move data safely across changes."
---

# Purpose
Guide schema and data migration strategy for Odoo changes, including upgrade scripts, noupdate handling, and version transitions.

# Primary routing rule
Use this skill only when the primary requested output is migration or upgrade strategy. If the user mainly wants command semantics, use `odoo-delivery-ops`.

# Use this skill when
- rename fields or models
- move data between modules
- write upgrade or migration scripts
- plan module or version upgrades

# Do not use this skill when
- the change has no schema or data evolution
- the question is only about runtime flags
- the task is ordinary feature build without migration risk

# Required inputs
Question or artifact, module/entrypoint if known, surrounding context when available.

# Workflow
Confirm → Read anchors → Apply checklist → Answer with guidance → State boundary decision.

# Output contract
- migration approach
- script or data-move notes
- validation checklist
- rollout cautions
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only this skill's domain. Anchor to Odoo docs + CE source, not generic ERP intuition.
- Highlight cross-app, accounting, or security effects. Redirect to task skills for planning/building/testing/shipping.

# Must hand off when
- If the user asks low-level update or worker semantics, hand off to `odoo-delivery-ops`.
- If the user asks whether a release is ready, compose with `odoo-ship`.
- If the change is still being planned, compose with `odoo-plan`.

# Compose with sibling skills
- `odoo-ship`
- `odoo-plan`
- `odoo-delivery-ops`

# References
`references/overview.md` (scope + anchors) · `references/checklist.md` · `references/examples.md`
