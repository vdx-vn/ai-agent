---
name: odoo-business-expenses
description: "Explain Odoo expense submission, approval, posting, and reimbursement flow together with HR and accounting links. Use when the primary entrypoint is expense claim, expense sheet, reimbursement, or posting, even if HR actors are involved."
---

# Purpose
Explain Odoo expense flow from submission through approval, posting, and reimbursement, including HR and accounting links.

# Primary routing rule
Use this skill only when the primary business entrypoint is expense claim, expense sheet, reimbursement, or expense posting. If the entrypoint is employee contract, attendance, time off, or payroll prerequisite, use `odoo-business-hr`.

# Use this skill when
- explain expense-sheet process impact
- trace expense approval into accounting
- reason about employee-paid or company-paid reimbursement behavior

# Do not use this skill when
- the primary entrypoint is employee master data or payroll prerequisite
- the task is generic AP or vendor-bill flow
- the issue is pure technical field design

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
- base expense flow
- cross-app impacts
- roles and decision points
- golden-path test ideas
- boundary decision with primary skill, composed siblings, and deferred scope

# Guardrails
- Answer only the domain or technical question this skill owns.
- Use Odoo <ODOO_MAJOR_VERSION> docs as guidance and Odoo CE <ODOO_MAJOR_VERSION> source as runtime truth.
- Do not answer from generic ERP intuition; anchor to Odoo <ODOO_MAJOR_VERSION> terms, addons, and bridge modules.
- Highlight cross-app, accounting, or security effects when they materially change the answer.
- Redirect to task skills when the user needs planning, building, testing, or shipping.

# Must hand off when
- If the question is mainly about employee contract, attendance, or payroll prerequisites, hand off to `odoo-business-hr`.
- If finance posting dominates after approval, compose with `odoo-business-accounting`.
- If permissions or exposure dominate, compose with `odoo-security`.

# Compose with sibling skills
- `odoo-business-hr`
- `odoo-business-accounting`
- `odoo-security`

# References
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
