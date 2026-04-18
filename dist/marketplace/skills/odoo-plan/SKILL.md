---
name: odoo-plan
description: "Turn Odoo requests into execution plans. Use when the primary output is an ordered plan with file and module mapping, acceptance criteria, test strategy, rollout notes, and open decisions. Do not use for code changes."
---

# Purpose
Convert an Odoo request into an execution plan with files, modules, acceptance criteria, validation, rollout notes, and unresolved decisions.

# Primary routing rule
Use this skill only when the user wants a plan artifact. If the user wants a risk brief, use `odoo-think`. If the user wants code edits, use `odoo-build`.

# Use this skill when
- build a step-by-step implementation plan
- identify files, modules, tests, and rollout notes before coding
- define acceptance criteria and unresolved design decisions
- turn scoped work into an actionable execution sequence

# Do not use this skill when
- the primary requested output is only impact analysis or risk discovery
- the user wants direct implementation or patch generation
- the task is a retrospective or release go or no-go call

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
- ordered implementation steps
- target files and modules
- acceptance criteria and open decisions
- test matrix and rollout notes
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Stay inside this sprint-phase responsibility; do not absorb neighboring tasks.
- Prefer current Odoo docs for functional rules and current Odoo CE source for implementation truth.
- Call out docs or source mismatches instead of hiding them.
- Name permissions impact, migration impact, and cross-app modules whenever relevant.
- Name rollback or staging risk whenever release or data impact exists.
- Keep this skill at planning depth; do not drift into code generation.

# Must hand off when
- If the user asks for code, XML, manifest, or security changes now, hand off to `odoo-build`.
- If migration strategy becomes central, compose with `odoo-upgrade-migration`.
- If the scope is still unclear, step back to `odoo-think`.

# Compose with sibling skills
- `odoo-think`
- `odoo-build`
- `odoo-test`
- `odoo-upgrade-migration`

# References
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
