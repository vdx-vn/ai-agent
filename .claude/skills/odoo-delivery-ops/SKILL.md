---
name: odoo-delivery-ops
description: "Guide Odoo CLI and runtime operations, including odoo-bin flags, module update and install semantics, worker settings, and Odoo.sh stage behavior. Use when the primary question is command semantics or environment mechanics, not release readiness."
---

# Purpose
Guide Odoo CLI, runtime, and environment behavior, especially install or update semantics, workers, and Odoo.sh stage mechanics.

# Primary routing rule
Use this skill only when the primary requested output is command, flag, worker, or environment semantics. If the user asks whether a release is ready, use `odoo-ship`.

# Use this skill when
- interpret odoo-bin flags and module update semantics
- choose worker or runtime settings
- understand Odoo.sh stage and branch behavior

# Do not use this skill when
- the primary requested output is migration strategy
- the task is general release-readiness narrative
- the request is purely business-process explanation

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
- command or flag guidance
- runtime cautions
- environment notes
- follow-up release checks
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only the domain or technical question this skill owns.
- Use Odoo <ODOO_MAJOR_VERSION> docs as guidance and Odoo CE <ODOO_MAJOR_VERSION> source as runtime truth.
- Do not answer from generic ERP intuition; anchor to Odoo <ODOO_MAJOR_VERSION> terms, addons, and bridge modules.
- Highlight cross-app, accounting, or security effects when they materially change the answer.
- Redirect to task skills when the user needs planning, building, testing, or shipping.

# Must hand off when
- If the user asks whether the change is ready to ship, hand off to `odoo-ship`.
- If schema or data evolution is central, hand off to `odoo-upgrade-migration`.
- If test evidence is still missing, compose with `odoo-test`.

# Compose with sibling skills
- `odoo-ship`
- `odoo-test`
- `odoo-upgrade-migration`

# References
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
