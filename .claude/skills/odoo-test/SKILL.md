---
name: odoo-test
description: "Validate a concrete Odoo change with install, update, workflow, security, and performance checks. Use when the primary output should be current validation evidence or a current-change validation plan, not general framework guidance."
---

# Purpose
Define and run validation for a current Odoo change, including install, update, workflow, security, and performance checks.

# Primary routing rule
Use this skill only when the primary requested output is validation for a concrete change now. If the user asks which Odoo test framework or tags to use in general, hand off to `odoo-testing-reference`.

# Use this skill when
- run or choose validation for current Odoo work
- validate install, update, or regression behavior for a concrete change
- prepare confidence signal before merge or release
- triage failing validation for current work

# Do not use this skill when
- the primary requested output is framework theory or future test-authoring advice
- the task is code review without validation evidence
- the task is deployment orchestration only

# Required inputs
- user request and desired output artifact
- target module(s), files, or flow if known
- current diff, traceback, failing scenario, or release context when available

# Workflow
1. Confirm the requested output artifact belongs in this skill; redirect if it does not.
2. Map the request to the smallest relevant Odoo modules, docs, and source anchors.
3. Apply the deterministic checks in `references/checklist.md`.
4. Produce the artifact described below, naming assumptions, blockers, and cross-app effects.
5. Hand off or compose with sibling skills when the request crosses this skill boundary.

# Output contract
- test matrix
- commands or suites run
- observed failures
- remaining validation gaps

# Guardrails
- Stay inside this sprint-phase responsibility; do not absorb neighboring tasks.
- Prefer Odoo <ODOO_MAJOR_VERSION> docs for functional rules and Odoo CE <ODOO_MAJOR_VERSION> source for implementation truth.
- Call out docs or source mismatches instead of hiding them.
- Name permissions impact, migration impact, and cross-app modules whenever relevant.
- Name rollback or staging risk whenever release or data impact exists.

# Must hand off when
- If the user asks how Odoo testing primitives work in general, hand off to `odoo-testing-reference`.
- If the ask is a pre-merge reasoning review rather than evidence, hand off to `odoo-review`.
- Compose with business skills when workflow validation depends on domain process.

# Compose with sibling skills
- `odoo-testing-reference`
- `odoo-performance`

# References
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
