# Checklist

## Intake
- [ ] Confirm the requested artifact belongs to `odoo-business-hr`.
- [ ] Identify main module, bridge module, or business or technical entrypoint.
- [ ] Identify adjacent skills needed for composition.
- [ ] Identify nearest-neighbor skill and why it does not own the request.

## Analysis
- [ ] Identify HR entrypoint: employee, contract, attendance, time off, planning, or payroll prerequisite.
- [ ] Trace work-entry and approval implications.
- [ ] Mention HR links to timesheets, expenses, and payroll prerequisites.
- [ ] Call out role and compliance sensitivities.

## Production readiness
- [ ] Identify the business entrypoint before tracing the flow.
- [ ] Trace downstream documents and approvals.
- [ ] Name cross-app bridges, accounting effects, and security or role implications.
- [ ] Keep implementation details out unless they change process meaning.

## Output
- [ ] Return base HR flow
- [ ] Return cross-app impacts
- [ ] Return roles and decision points
- [ ] Return golden-path test ideas
- [ ] Return boundary decision
- [ ] Name assumptions, blockers, or missing context.
- [ ] Redirect clearly if the request crosses this skill boundary.
