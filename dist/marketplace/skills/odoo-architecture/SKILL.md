---
name: odoo-architecture
description: "Guide Odoo module boundaries, dependency graph, inheritance placement, and bridge-module strategy. Use when the primary output is an addon-placement or dependency decision, not field semantics or business-flow explanation."
---

# Purpose
Guide module boundaries, dependency graph, inheritance strategy, and bridge-module placement for Odoo addons.

# Primary routing rule
Use this skill only when the primary requested output is an addon-placement or dependency decision.

# Use this skill when
- decide where code should live
- design addon dependencies or inheritance strategy
- decide between extending an addon and creating a bridge module

# Do not use this skill when
- the primary requested output is field or ORM semantics
- the question is an access-control policy
- the user needs business-process explanation only

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
- recommended addon location
- dependency rationale
- bridge-module or extension guidance
- architecture risks
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only the domain or technical question this skill owns.
- Use current Odoo docs as guidance and current Odoo CE source as runtime truth.
- Do not answer from generic ERP intuition; anchor to current Odoo terms, addons, and bridge modules.
- Highlight cross-app, accounting, or security effects when they materially change the answer.
- Redirect to task skills when the user needs planning, building, testing, or shipping.

# Must hand off when
- If the user wants an implementation plan, hand off to `odoo-plan`.
- If the question is mainly about field or decorator behavior, hand off to `odoo-orm-modeling`.
- Compose with business skills when placement depends on the process entrypoint.

# Compose with sibling skills
- `odoo-plan`
- `odoo-build`
- `odoo-orm-modeling`

# References
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
