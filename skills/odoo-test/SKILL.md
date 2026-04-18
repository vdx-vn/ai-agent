---
name: odoo-test
description: "Validate a concrete Odoo change with install, update, workflow, security, and performance checks. Compose with `odoo-local-test-harness` when local execution depends on a project-specific base Odoo test command or shared DB and filestore cleanup."
---

# Purpose
Define and run validation for a current Odoo change, including install, update, workflow, security, and performance checks.

# Primary routing rule
Use this skill only when the primary requested output is validation for a concrete change now. If the user asks which Odoo test framework or tags to use in general, hand off to `odoo-testing-reference`. If the user wants findings on an existing artifact without execution, use `odoo-review`.

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
5. State a boundary decision with primary skill, composed siblings, and deferred scope.

# Output contract
- evidence status: executed, planned, or blocked
- test matrix
- commands or suites run
- observed failures or outcomes
- remaining validation gaps
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Stay inside this sprint-phase responsibility; do not absorb neighboring tasks.
- Prefer current Odoo docs for functional rules and current Odoo CE source for implementation truth.
- Call out docs or source mismatches instead of hiding them.
- Name permissions impact, migration impact, and cross-app modules whenever relevant.
- Name rollback or staging risk whenever release or data impact exists.
- Separate executed evidence from planned validation. If nothing ran, say so plainly.

# Must hand off when
- If the user asks how Odoo testing primitives work in general, hand off to `odoo-testing-reference`.
- If the ask is a pre-merge reasoning review rather than validation evidence, hand off to `odoo-review`.
- Compose with business skills when workflow validation depends on domain process.
- If local execution depends on a project-specific base command or shared cleanup harness, compose with `odoo-local-test-harness`.

# Compose with sibling skills
- `odoo-review`
- `odoo-testing-reference`
- `odoo-performance`
- `odoo-local-test-harness`

# References
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
