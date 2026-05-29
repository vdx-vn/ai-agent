---
name: odoo-delivery-ops
description: "Guide Odoo CLI and runtime operations, including odoo-bin flags, module update and install semantics, worker settings, and Odoo.sh stage behavior. Compose with `odoo-local-test-harness` when a local project-specific base test command is part of the answer."
---

# Purpose
Guide Odoo CLI, runtime, and environment behavior, especially install or update semantics, workers, and Odoo.sh stage mechanics.

# Primary routing rule
Use this skill only when the primary requested output is command, flag, worker, or environment semantics. If the user asks whether a release is ready, use `odoo-ship`.

# Use this skill when
- interpret odoo-bin flags and module update semantics
- choose worker or runtime settings
- understand Odoo.sh stage and branch behavior

# Do not use this skill when
- the primary requested output is migration strategy
- the task is general release-readiness narrative
- the request is purely business-process explanation

# Required inputs
Question or artifact, module/entrypoint if known, surrounding context when available.

# Workflow
Confirm → Read anchors → Apply checklist → Answer with guidance → State boundary decision.

# Output contract
- command or flag guidance
- runtime cautions
- environment notes
- follow-up release checks
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only this skill's domain. Anchor to Odoo docs + CE source, not generic ERP intuition.
- Highlight cross-app, accounting, or security effects. Redirect to task skills for planning/building/testing/shipping.

# Must hand off when
- If the user asks whether the change is ready to ship, hand off to `odoo-ship`.
- If schema or data evolution is central, hand off to `odoo-upgrade-migration`.
- If test evidence is still missing, compose with `odoo-test`.
- If the answer depends on a project-local base Odoo test command or shared local cleanup harness, compose with `odoo-local-test-harness`.

# Compose with sibling skills
- `odoo-ship`
- `odoo-test`
- `odoo-upgrade-migration`
- `odoo-local-test-harness`

# References
`references/overview.md` (scope + anchors) · `references/checklist.md` · `references/examples.md`
