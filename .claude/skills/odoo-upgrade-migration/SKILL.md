---
name: odoo-upgrade-migration
description: "Guide Odoo schema, data, and module upgrades, migration scripts, custom DB upgrade steps, and noupdate handling. Use when the primary question is how to preserve and move data safely across changes."
---

# Purpose
Guide schema and data migration strategy for Odoo changes, including upgrade scripts, noupdate handling, and version transitions.

# Primary routing rule
Use this skill only when the primary requested output is migration or upgrade strategy. If the user mainly wants command semantics, use `odoo-delivery-ops`.

# Use this skill when
- rename fields or models
- move data between modules
- write upgrade or migration scripts
- plan module or version upgrades

# Do not use this skill when
- the change has no schema or data evolution
- the question is only about runtime flags
- the task is ordinary feature build without migration risk

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
- migration approach
- script or data-move notes
- validation checklist
- rollout cautions
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only the domain or technical question this skill owns.
- Use Odoo <ODOO_MAJOR_VERSION> docs as guidance and Odoo CE <ODOO_MAJOR_VERSION> source as runtime truth.
- Do not answer from generic ERP intuition; anchor to Odoo <ODOO_MAJOR_VERSION> terms, addons, and bridge modules.
- Highlight cross-app, accounting, or security effects when they materially change the answer.
- Redirect to task skills when the user needs planning, building, testing, or shipping.

# Must hand off when
- If the user asks low-level update or worker semantics, hand off to `odoo-delivery-ops`.
- If the user asks whether a release is ready, compose with `odoo-ship`.
- If the change is still being planned, compose with `odoo-plan`.

# Compose with sibling skills
- `odoo-ship`
- `odoo-plan`
- `odoo-delivery-ops`

# References
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
