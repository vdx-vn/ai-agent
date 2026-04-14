---
name: odoo-ship
description: "Prepare Odoo changes for staging or release. Use when the primary output should be go or no-go readiness, rollout sequencing, staging checks, rollback considerations, and production-facing cautions, not low-level command semantics."
---

# Purpose
Prepare release readiness for Odoo changes, including go or no-go criteria, staging checks, rollout sequencing, rollback considerations, and production-facing cautions.

# Primary routing rule
Use this skill only when the user wants release readiness or rollout sequencing. If the user needs CLI flag semantics or environment mechanics, hand off to `odoo-delivery-ops`. If the primary issue is data or schema evolution, compose with `odoo-upgrade-migration`.

# Use this skill when
- prepare staging or production release
- build deployment or rollout checklist
- decide whether current work is ready to ship
- identify rollback, migration, or production risk before release

# Do not use this skill when
- the primary requested output is low-level CLI or runtime semantics
- the task is still design or implementation
- the task is retrospective only

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
- go or no-go readiness summary
- ship checklist and rollout sequence
- staging verification list
- rollback or production cautions

# Guardrails
- Stay inside this sprint-phase responsibility; do not absorb neighboring tasks.
- Prefer Odoo <ODOO_MAJOR_VERSION> docs for functional rules and Odoo CE <ODOO_MAJOR_VERSION> source for implementation truth.
- Call out docs or source mismatches instead of hiding them.
- Name permissions impact, migration impact, and cross-app modules whenever relevant.
- Name rollback or staging risk whenever release or data impact exists.

# Must hand off when
- If the user asks what `-u`, `-i`, `--reinit`, workers, or Odoo.sh stages do, hand off to `odoo-delivery-ops`.
- If schema or data migration strategy is central, compose with `odoo-upgrade-migration`.
- If validation evidence is still missing, compose with `odoo-test` before calling the change ready.

# Compose with sibling skills
- `odoo-delivery-ops`
- `odoo-upgrade-migration`
- `odoo-test`

# References
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
