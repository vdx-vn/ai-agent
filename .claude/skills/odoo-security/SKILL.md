---
name: odoo-security
description: "Guide deep Odoo security analysis across groups, ACL, record rules, public methods, controller auth, CSRF, sudo, SQL, XSS, and eval risks. Use when exposure, permissions, trust boundaries, or attack surface are central."
---

# Purpose
Guide Odoo security model including groups, ACL, record rules, controller auth, public methods, CSRF, sudo, SQL, XSS, and eval risks.

# Primary routing rule
Use this skill only when the primary requested output is a trust-boundary or exposure assessment. If the user wants a broad code review, use `odoo-review` and compose with this skill only when security is central.

# Use this skill when
- review access rights or record rules
- inspect controller auth, public routes, or CSRF behavior
- check sudo, SQL, XSS, or unsafe eval risks
- analyze data exposure or privilege-escalation paths

# Do not use this skill when
- the primary requested output is a generic code review with no security center of gravity
- the request is only business-flow explanation
- the question is mostly UI layout

# Required inputs
- user question or design decision
- current module, entrypoint, or artifact under discussion if known
- surrounding business or technical context when available

# Workflow
1. Confirm the requested decision or process belongs in this skill; redirect if it does not.
2. Read only the smallest relevant anchors from `references/overview.md`.
3. Apply the rule or process checklist in `references/checklist.md`.
4. Answer with Odoo-specific guidance, tradeoffs, downstream effects, and boundary notes.
5. Point to sibling skills when implementation workflow or adjacent domains matter.

# Output contract
- security findings
- access-control recommendations
- trust-boundary notes
- required tests or follow-ups

# Guardrails
- Answer only the domain or technical question this skill owns.
- Use Odoo <ODOO_MAJOR_VERSION> docs as guidance and Odoo CE <ODOO_MAJOR_VERSION> source as runtime truth.
- Do not answer from generic ERP intuition; anchor to Odoo <ODOO_MAJOR_VERSION> terms, addons, and bridge modules.
- Highlight cross-app, accounting, or security effects when they materially change the answer.
- Redirect to task skills when the user needs planning, building, testing, or shipping.

# Must hand off when
- If the user wants broad review findings on an entire diff, use `odoo-review` as primary and compose with `odoo-security`.
- If implementation changes are requested, compose with `odoo-build`.
- If the issue is mainly process ownership or roles, compose with the matching business skill.

# Compose with sibling skills
- `odoo-review`
- `odoo-build`

# References
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
