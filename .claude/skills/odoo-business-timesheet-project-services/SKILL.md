---
name: odoo-business-timesheet-project-services
description: "Explain Odoo services delivery across project, task, timesheet, planning, helpdesk, and sales invoicing links. Use when the primary entrypoint is service work, project tasks, or billable time."
---

# Purpose
Explain Odoo service-delivery flows across project, task, timesheet, planning, helpdesk, and sales invoicing links.

# Primary routing rule
Use this skill only when the primary business entrypoint is project, task, timesheet, helpdesk, planning, or service delivery.

# Use this skill when
- explain project, task, or timesheet process impact
- trace service delivery into invoicing
- map planning or helpdesk links to billable work

# Do not use this skill when
- the primary entrypoint is HR contract or payroll policy
- the request is pure expense reimbursement
- the issue is technical ORM or ACL design

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
- base service flow
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
- If workforce policy or payroll prerequisites dominate, compose with `odoo-business-hr`.
- If the main issue is finance posting, compose with `odoo-business-accounting`.
- If the primary entrypoint is backend quote or order rather than service delivery, compose with `odoo-business-sales`.

# Compose with sibling skills
- `odoo-business-sales`
- `odoo-business-hr`
- `odoo-business-accounting`

# References
- Read `references/overview.md` first for scope, anchors, and pairings.
- Use `references/checklist.md` for deterministic checks.
- Use `references/examples.md` to compare trigger, boundary, and tie-breaker prompts.
