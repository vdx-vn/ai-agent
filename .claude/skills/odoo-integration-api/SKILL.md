---
name: odoo-integration-api
description: "Guide external integration design for Odoo, including RPC and API patterns, bot users, auth, transaction boundaries, and idempotent business operations. Use when the primary question is external-system integration."
---

# Purpose
Guide Odoo external integration patterns, auth choices, RPC or HTTP approaches, and transaction boundaries for business operations.

# Primary routing rule
Use this skill only when the primary requested output is an external integration design or RPC or API decision.

# Use this skill when
- design a webhook or sync job
- connect Odoo to an external system
- decide auth and account model for an integration user

# Do not use this skill when
- the task is an internal-only module customization
- the question is mainly about UI layout
- the problem is generic ORM modeling

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
- integration pattern recommendation
- auth and user model
- transaction-boundary notes
- failure and retry considerations
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only the domain or technical question this skill owns.
- Use Odoo <ODOO_MAJOR_VERSION> docs as guidance and Odoo CE <ODOO_MAJOR_VERSION> source as runtime truth.
- Do not answer from generic ERP intuition; anchor to Odoo <ODOO_MAJOR_VERSION> terms, addons, and bridge modules.
- Highlight cross-app, accounting, or security effects when they materially change the answer.
- Redirect to task skills when the user needs planning, building, testing, or shipping.

# Must hand off when
- If the ask is about controller exposure or trust boundaries, compose with `odoo-security`.
- If the ask becomes runtime deployment mechanics, compose with `odoo-delivery-ops`.
- If the user wants code changes, hand off to `odoo-build`.

# Compose with sibling skills
- `odoo-security`
- `odoo-delivery-ops`
- `odoo-build`

# References
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
