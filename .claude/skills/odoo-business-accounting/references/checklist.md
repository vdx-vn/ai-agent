# Checklist

## Intake
- [ ] Confirm the requested artifact belongs to `odoo-business-accounting`.
- [ ] Identify main module, bridge module, or business or technical entrypoint.
- [ ] Identify adjacent skills needed for composition.
- [ ] Identify nearest-neighbor skill and why it does not own the request.

## Analysis
- [ ] Identify finance entrypoint: invoice, bill, payment, tax, reconciliation, or valuation.
- [ ] Trace upstream business documents and downstream reports.
- [ ] Mention crossovers from stock_account, hr_expense, or timesheets when relevant.
- [ ] Call out localization and fiscal-position concerns.

## Production readiness
- [ ] Identify the business entrypoint before tracing the flow.
- [ ] Trace downstream documents and approvals.
- [ ] Name cross-app bridges, accounting effects, and security or role implications.
- [ ] Keep implementation details out unless they change process meaning.

## Output
- [ ] Return base accounting flow
- [ ] Return cross-app impacts
- [ ] Return roles and decision points
- [ ] Return golden-path test ideas
- [ ] Return boundary decision
- [ ] Name assumptions, blockers, or missing context.
- [ ] Redirect clearly if the request crosses this skill boundary.
