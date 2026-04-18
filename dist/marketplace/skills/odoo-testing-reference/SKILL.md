---
name: odoo-testing-reference
description: "Explain Odoo test framework, test tags, TransactionCase, HttpCase, tours, and JS tests. Use only when the primary output is framework-selection or test-authoring guidance, not when judging whether current work is validated."
---

# Purpose
Explain Odoo test framework primitives, tagging, and test-design patterns without acting as the live test-execution workflow skill.

# Primary routing rule
Use this skill only when the primary requested output is framework or test-authoring guidance. If the user asks whether current work is tested or safe, use `odoo-test`.

# Use this skill when
- understand Odoo test tags and framework choices
- decide between TransactionCase, HttpCase, tours, and JS tests
- design an Odoo-specific test strategy or author a new test

# Do not use this skill when
- the primary requested output is validation for a current change
- the task is code review
- the question is about release readiness

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
- recommended test types
- relevant test tags
- framework-specific cautions
- example test shape
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only the domain or technical question this skill owns.
- Use current Odoo docs as guidance and current Odoo CE source as runtime truth.
- Do not answer from generic ERP intuition; anchor to current Odoo terms, addons, and bridge modules.
- Highlight cross-app, accounting, or security effects when they materially change the answer.
- Redirect to task skills when the user needs planning, building, testing, or shipping.

# Must hand off when
- If the user asks to validate a concrete diff or runtime behavior now, hand off to `odoo-test`.
- If the question is mostly UI or browser flow behavior, compose with `odoo-view-ui`.
- If the concern is query count or speed, compose with `odoo-performance`.

# Compose with sibling skills
- `odoo-test`
- `odoo-performance`
- `odoo-view-ui`

# References
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
