---
name: odoo-reflect
description: "Reflect on completed Odoo work. Use when the primary output is a retrospective with lessons learned, missed assumptions, and concrete follow-up actions after review, testing, or release."
---

# Purpose
Produce a retrospective for completed Odoo work, covering what happened, what was missed, and what follow-up actions remain.

# Primary routing rule
Use this skill only when the primary requested output is a retrospective or lessons learned artifact after work already happened.

# Use this skill when
- run a retrospective after review, testing, or release
- summarize lessons learned from an Odoo change
- identify follow-up hardening or debt after completion
- turn observed misses into concrete future actions

# Do not use this skill when
- the task is still active planning or implementation
- the request is live code review
- the task is test execution

# Required inputs
- user request and desired output artifact
- target module(s), files, or flow if known
- current diff, traceback, failing scenario, or release context when available

# Workflow
1. Confirm the requested output artifact belongs in this skill; redirect if it does not.
2. Map the request to the smallest relevant Odoo modules, docs, and source anchors.
3. Apply the deterministic checks in `references/checklist.md`.
4. Produce the artifact described below, naming assumptions, blockers, and cross-app effects.
5. State a boundary decision with primary skill, composed siblings, and deferred scope.

# Output contract
- summary of what happened
- gaps or misses
- lessons learned
- follow-up tasks
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Stay inside this sprint-phase responsibility; do not absorb neighboring tasks.
- Prefer Odoo <ODOO_MAJOR_VERSION> docs for functional rules and Odoo CE <ODOO_MAJOR_VERSION> source for implementation truth.
- Call out docs or source mismatches instead of hiding them.
- Name permissions impact, migration impact, and cross-app modules whenever relevant.
- Name rollback or staging risk whenever release or data impact exists.
- Produce concrete lessons and follow-up actions, not vague commentary.

# Must hand off when
- If the user is still deciding what to build, hand off to `odoo-think` or `odoo-plan`.
- If the user wants findings on a current diff, hand off to `odoo-review`.
- Compose with business skills when the lesson depends on domain process misunderstanding.

# Compose with sibling skills
- `odoo-think`
- `odoo-plan`
- `odoo-review`
- `odoo-test`

# References
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
