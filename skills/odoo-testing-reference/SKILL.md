---
name: odoo-testing-reference
description: "Explain Odoo test framework, test tags, TransactionCase, HttpCase, tours, and JS tests. Use only when the primary output is framework-selection or test-authoring guidance, not when judging whether current work is validated."
---

# Purpose
Explain Odoo test framework primitives, tagging, and test-design patterns without acting as the live test-execution workflow skill.

# Primary routing rule
Use this skill only when the primary requested output is framework or test-authoring guidance. If the user asks whether current work is tested or safe, use `odoo-test`.

# Use this skill when
- understand Odoo test tags and framework choices
- decide between TransactionCase, HttpCase, tours, and JS tests
- design an Odoo-specific test strategy or author a new test

# Do not use this skill when
- the primary requested output is validation for a current change
- the task is code review
- the question is about release readiness

# Required inputs
Question or artifact, module/entrypoint if known, surrounding context when available.

# Workflow
Confirm → Read anchors → Apply checklist → Answer with guidance → State boundary decision.

# Output contract
- recommended test types
- relevant test tags
- framework-specific cautions
- example test shape
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only this skill's domain. Anchor to Odoo docs + CE source, not generic ERP intuition.
- Highlight cross-app, accounting, or security effects. Redirect to task skills for planning/building/testing/shipping.

# Must hand off when
- If the user asks to validate a concrete diff or runtime behavior now, hand off to `odoo-test`.
- If the question is mostly UI or browser flow behavior, compose with `odoo-view-ui`.
- If the concern is query count or speed, compose with `odoo-performance`.

# Compose with sibling skills
- `odoo-test`
- `odoo-performance`
- `odoo-view-ui`

# References
`references/overview.md` (scope + anchors) · `references/checklist.md` · `references/examples.md`
