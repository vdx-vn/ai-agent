---
name: odoo-architecture
description: "Guide Odoo module boundaries, dependency graph, inheritance placement, and bridge-module strategy. Use when the primary output is an addon-placement or dependency decision, not field semantics or business-flow explanation."
---

# Purpose
Guide module boundaries, dependency graph, inheritance strategy, and bridge-module placement for Odoo addons.

# Primary routing rule
Use this skill only when the primary requested output is an addon-placement or dependency decision.

# Use this skill when
- decide where code should live
- design addon dependencies or inheritance strategy
- decide between extending an addon and creating a bridge module

# Do not use this skill when
- the primary requested output is field or ORM semantics
- the question is an access-control policy
- the user needs business-process explanation only

# Required inputs
Question or artifact, module/entrypoint if known, surrounding context when available.

# Workflow
Confirm → Read anchors → Apply checklist → Answer with guidance → State boundary decision.

# Output contract
- recommended addon location
- dependency rationale
- bridge-module or extension guidance
- architecture risks
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only this skill's domain. Anchor to Odoo docs + CE source, not generic ERP intuition.
- Highlight cross-app, accounting, or security effects. Redirect to task skills for planning/building/testing/shipping.

# Must hand off when
- If the user wants an implementation plan, hand off to `odoo-plan`.
- If the question is mainly about field or decorator behavior, hand off to `odoo-orm-modeling`.
- Compose with business skills when placement depends on the process entrypoint.

# Compose with sibling skills
- `odoo-plan`
- `odoo-build`
- `odoo-orm-modeling`

# References
`references/overview.md` (scope + anchors) · `references/checklist.md` · `references/examples.md`
