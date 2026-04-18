---
name: odoo-review
description: "Review existing Odoo changes before merge. Use when the primary output is review findings on a diff, patch, or implementation artifact about architecture fit, maintainability, correctness, and broad risk. Do not use when the main ask is to execute validation."
---

# Purpose
Review an existing Odoo change artifact for architecture fit, maintainability, correctness, broad risk, and cross-app impact before merge.

# Primary routing rule
Use this skill only when the primary requested output is review findings on an existing artifact. If the user wants executed validation evidence, use `odoo-test`. If the prompt centers on exposure or trust boundaries, compose with or defer to `odoo-security`.

# Use this skill when
- review a diff or patch before merge
- check architecture fit, maintainability, and broad risk
- find issues in an implemented change artifact
- perform pre-merge structural review

# Do not use this skill when
- the primary requested output is executed validation or regression evidence
- no diff, patch, or implemented artifact exists yet
- the task is a retrospective after completion

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
- evidence status: reasoned review only
- findings by severity
- required fixes
- suggested improvements
- untested risk areas
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Stay inside this sprint-phase responsibility; do not absorb neighboring tasks.
- Prefer Odoo <ODOO_MAJOR_VERSION> docs for functional rules and Odoo CE <ODOO_MAJOR_VERSION> source for implementation truth.
- Call out docs or source mismatches instead of hiding them.
- Name permissions impact, migration impact, and cross-app modules whenever relevant.
- Name rollback or staging risk whenever release or data impact exists.
- Do not imply commands were run or validation evidence exists unless execution evidence is provided separately.

# Must hand off when
- If there is no artifact yet, hand off to `odoo-think` or `odoo-plan`.
- If the user asks to run validation or produce execution evidence, hand off to `odoo-test`.
- If permissions, exposure, or trust boundaries are central, compose with `odoo-security`.

# Compose with sibling skills
- `odoo-think`
- `odoo-plan`
- `odoo-security`
- `odoo-test`
- `odoo-testing-reference`

# References
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
