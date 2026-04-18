---
name: odoo-think
description: "Diagnose Odoo request scope before planning. Use when the primary output is a scoping brief with impacted modules, business entrypoints, risks, unknowns, and decision framing. Do not use for implementation steps or code changes."
---

# Purpose
Frame the request, identify impacted modules, business entrypoints, risks, and unknowns before any execution plan or implementation begins.

# Primary routing rule
Use this skill only when the primary requested output is a scoping brief or impact diagnosis. If the user wants ordered steps, file-by-file actions, or acceptance criteria, hand off to `odoo-plan`.

# Use this skill when
- scope a request before planning
- identify affected modules, bridge addons, or business entrypoints
- surface major technical, security, accounting, inventory, payroll, or upgrade risks
- clarify unknowns that block a safe plan

# Do not use this skill when
- the primary requested output is an execution plan
- the user is asking to implement or patch code now
- the task is review, testing, shipping, or retrospective work

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
- problem statement
- impacted modules and bridge addons
- affected business flow and entrypoint
- top risks and unknowns
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Stay inside this sprint-phase responsibility; do not absorb neighboring tasks.
- Prefer current Odoo docs for functional rules and current Odoo CE source for implementation truth.
- Call out docs or source mismatches instead of hiding them.
- Name permissions impact, migration impact, and cross-app modules whenever relevant.
- Name rollback or staging risk whenever release or data impact exists.
- Do not drift into ordered implementation steps or code changes.

# Must hand off when
- If the user asks for ordered implementation steps, files, or acceptance criteria, hand off to `odoo-plan`.
- If the user asks for concrete code changes, hand off to `odoo-build`.
- If the question is mainly business-process meaning, compose with the matching business skill.

# Compose with sibling skills
- `odoo-plan`
- `odoo-build`
- `odoo-architecture`

# References
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
