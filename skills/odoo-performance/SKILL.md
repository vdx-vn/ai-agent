---
name: odoo-performance
description: "Guide Odoo performance analysis: batching, query count, complexity, indexing, profiler usage, and cache or prefetch patterns. Use when the primary question is hotspot diagnosis or scaling behavior."
---

# Purpose
Guide performance analysis and optimization for Odoo code, especially ORM-heavy, query-heavy, and batch-heavy paths.

# Primary routing rule
Use this skill only when the primary requested output is performance diagnosis or optimization guidance.

# Use this skill when
- investigate slow queries or N+1 issues
- review batching and indexing strategy
- choose profiler or query-count validation for Odoo paths

# Do not use this skill when
- the primary requested output is generic ORM semantics without a performance angle
- the task is a release checklist
- the request is pure business-flow explanation

# Required inputs
Question or artifact, module/entrypoint if known, surrounding context when available.

# Workflow
Confirm → Read anchors → Apply checklist → Answer with guidance → State boundary decision.

# Output contract
- likely hotspots
- optimization recommendations
- measurement or profiler plan
- performance-test notes
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only this skill's domain. Anchor to Odoo docs + CE source, not generic ERP intuition.
- Highlight cross-app, accounting, or security effects. Redirect to task skills for planning/building/testing/shipping.

# Must hand off when
- If the ask becomes about general field or decorator semantics, hand off to `odoo-orm-modeling`.
- If the user wants validation evidence for a current change, compose with `odoo-test`.
- If the question is broad code quality review, compose with `odoo-review`.

# Compose with sibling skills
- `odoo-test`
- `odoo-orm-modeling`
- `odoo-review`

# References
`references/overview.md` (scope + anchors) · `references/checklist.md` · `references/examples.md`
