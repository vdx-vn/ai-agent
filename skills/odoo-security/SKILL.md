---
name: odoo-security
description: "Guide deep Odoo security analysis across groups, ACL, record rules, public methods, controller auth, CSRF, sudo, SQL, XSS, and eval risks. Use when exposure, permissions, trust boundaries, or attack surface are central."
---

# Purpose
Guide Odoo security model including groups, ACL, record rules, controller auth, public methods, CSRF, sudo, SQL, XSS, and eval risks.

# Primary routing rule
Use this skill only when the primary requested output is a trust-boundary or exposure assessment. If the user wants a broad code review, use `odoo-review` and compose with this skill only when security is central.

# Use this skill when
- review access rights or record rules
- inspect controller auth, public routes, or CSRF behavior
- check sudo, SQL, XSS, or unsafe eval risks
- analyze data exposure or privilege-escalation paths

# Do not use this skill when
- the primary requested output is a generic code review with no security center of gravity
- the request is only business-flow explanation
- the question is mostly UI layout

# Required inputs
Question or artifact, module/entrypoint if known, surrounding context when available.

# Workflow
Confirm → Read anchors → Apply checklist → Answer with guidance → State boundary decision.

# Output contract
- security findings
- access-control recommendations
- trust-boundary notes
- required tests or follow-ups
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only this skill's domain. Anchor to Odoo docs + CE source, not generic ERP intuition.
- Highlight cross-app, accounting, or security effects. Redirect to task skills for planning/building/testing/shipping.

# Must hand off when
- If the user wants broad review findings on an entire diff, use `odoo-review` as primary and compose with `odoo-security`.
- If implementation changes are requested, compose with `odoo-build`.
- If the issue is mainly process ownership or roles, compose with the matching business skill.

# Compose with sibling skills
- `odoo-review`
- `odoo-build`
- `odoo-security`

# References
`references/overview.md` (scope + anchors) · `references/checklist.md` · `references/examples.md`
