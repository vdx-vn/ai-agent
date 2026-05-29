---
name: odoo-integration-api
description: "Guide external integration design for Odoo, including RPC and API patterns, bot users, auth, transaction boundaries, and idempotent business operations. Use when the primary question is external-system integration."
---

# Purpose
Guide Odoo external integration patterns, auth choices, RPC or HTTP approaches, and transaction boundaries for business operations.

# Primary routing rule
Use this skill only when the primary requested output is an external integration design or RPC or API decision.

# Use this skill when
- design a webhook or sync job
- connect Odoo to an external system
- decide auth and account model for an integration user

# Do not use this skill when
- the task is an internal-only module customization
- the question is mainly about UI layout
- the problem is generic ORM modeling

# Required inputs
Question or artifact, module/entrypoint if known, surrounding context when available.

# Workflow
Confirm → Read anchors → Apply checklist → Answer with guidance → State boundary decision.

# Output contract
- integration pattern recommendation
- auth and user model
- transaction-boundary notes
- failure and retry considerations
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only this skill's domain. Anchor to Odoo docs + CE source, not generic ERP intuition.
- Highlight cross-app, accounting, or security effects. Redirect to task skills for planning/building/testing/shipping.

# Must hand off when
- If the ask is about controller exposure or trust boundaries, compose with `odoo-security`.
- If the ask becomes runtime deployment mechanics, compose with `odoo-delivery-ops`.
- If the user wants code changes, hand off to `odoo-build`.

# Compose with sibling skills
- `odoo-security`
- `odoo-delivery-ops`
- `odoo-build`

# References
`references/overview.md` (scope + anchors) · `references/checklist.md` · `references/examples.md`
