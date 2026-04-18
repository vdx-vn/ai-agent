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
- user question or design decision
- current module, entrypoint, or artifact under discussion if known
- surrounding business or technical context when available

# Workflow
1. Confirm the requested decision or process belongs in this skill; redirect if it does not.
2. Read only the smallest relevant anchors from `references/overview.md`.
3. Apply the rule or process checklist in `references/checklist.md`.
4. Answer with Odoo-specific guidance, tradeoffs, downstream effects, and boundary notes.
5. State a boundary decision with primary skill, composed siblings, and deferred scope.

# Output contract
- likely hotspots
- optimization recommendations
- measurement or profiler plan
- performance-test notes
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only the domain or technical question this skill owns.
- Use Odoo <ODOO_MAJOR_VERSION> docs as guidance and Odoo CE <ODOO_MAJOR_VERSION> source as runtime truth.
- Do not answer from generic ERP intuition; anchor to Odoo <ODOO_MAJOR_VERSION> terms, addons, and bridge modules.
- Highlight cross-app, accounting, or security effects when they materially change the answer.
- Redirect to task skills when the user needs planning, building, testing, or shipping.

# Must hand off when
- If the ask becomes about general field or decorator semantics, hand off to `odoo-orm-modeling`.
- If the user wants validation evidence for a current change, compose with `odoo-test`.
- If the question is broad code quality review, compose with `odoo-review`.

# Compose with sibling skills
- `odoo-test`
- `odoo-orm-modeling`
- `odoo-review`

# References
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
