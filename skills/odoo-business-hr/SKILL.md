---
name: odoo-business-hr
description: "Explain Odoo HR processes across employees, contracts, attendances, time off, payroll prerequisites, and related HR app interactions. Use when the primary entrypoint is employee, contract, attendance, time off, or workforce policy, not an expense claim lifecycle."
---

# Purpose
Explain Odoo HR processes around employees, attendances, time off, contracts, payroll prerequisites, and related app interactions.

# Primary routing rule
Use this skill only when the primary business entrypoint is employee, contract, attendance, time off, planning, or payroll prerequisite. If the entrypoint is expense claim, expense sheet, reimbursement, or posting, use `odoo-business-expenses`.

# Use this skill when
- explain employee, attendance, time-off, or HR-process impact
- reason about payroll prerequisites or work-entry inputs
- map HR app interactions around employee data and policy

# Do not use this skill when
- the primary entrypoint is expense claim lifecycle
- the request is project or service billing only
- the issue is technical security or ORM design

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
- base HR flow
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
- If the entrypoint is expense claim, sheet approval, reimbursement, or posting, hand off to `odoo-business-expenses`.
- If the question is about billable time or project delivery, compose with `odoo-business-timesheet-project-services`.
- If finance posting dominates, compose with `odoo-business-accounting`.

# Compose with sibling skills
- `odoo-business-timesheet-project-services`
- `odoo-business-expenses`
- `odoo-business-accounting`

# References
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
