---
name: odoo-test
description: "Validate a concrete Odoo change with install, update, workflow, security, and performance checks. Run tests with `odoo runtime-test` (odoo-cli), installed in the project's Python environment — the only supported test-execution command."
---

# Purpose
Define and run validation for a current Odoo change, including install, update, workflow, security, and performance checks.

# Primary routing rule
Use this skill only when the primary requested output is validation for a concrete change now. If the user asks which Odoo test framework or tags to use in general, hand off to `odoo-testing-reference`. If the user wants findings on an existing artifact without execution, use `odoo-review`.

# Use this skill when
- run or choose validation for current Odoo work
- plan install, update, workflow, security, and performance validation for current work
- run `odoo runtime-test` against a named database for the module(s) under change
- prepare confidence signal before merge or release
- triage failing validation for current work

# Do not use this skill when
- the primary requested output is framework theory or future test-authoring advice
- the task is code review without validation evidence
- the task is deployment orchestration only

# Required inputs
Artifact + target module/files if known + diff/traceback/context when available.

# Workflow
Confirm → Map to Odoo modules/anchors → Apply checklist → Run `odoo runtime-test` → Produce artifact → State boundary decision.

# Output contract
- evidence status: executed, planned, or blocked
- test matrix
- exact `odoo runtime-test` invocation(s) run
- `output_file` from the run's condensed JSON summary
- observed failures or outcomes
- remaining validation gaps
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Stay in sprint-phase scope; do not absorb neighbors.
- Anchor to Odoo docs (functional rules) and CE source (implementation truth); call out mismatches.
- Name permissions, migration, cross-app, and rollback risks when relevant.
- Separate executed evidence from planned validation. If nothing ran, say so plainly.
- `odoo runtime-test` is the only supported test-execution command; do not invoke `odoo-bin`/pytest-odoo directly or hand-roll a test-run script.

# Must hand off when
- If the user asks how Odoo testing primitives work in general, hand off to `odoo-testing-reference`.
- If the ask is a pre-merge reasoning review rather than validation evidence, hand off to `odoo-review`.
- Compose with business skills when workflow validation depends on domain process.

# Compose with sibling skills
- `odoo-review`
- `odoo-testing-reference`
- `odoo-performance`

# References
`references/overview.md` (scope + anchors) · `references/checklist.md` · `references/examples.md`
