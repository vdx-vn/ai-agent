# Checklist

## Intake
- [ ] Confirm the requested artifact belongs to `odoo-business-expenses`.
- [ ] Identify main module, bridge module, or business or technical entrypoint.
- [ ] Identify adjacent skills needed for composition.

## Analysis
- [ ] Identify expense state and actor: employee, manager, accountant.
- [ ] Trace sheet approval to posting and reimbursement.
- [ ] Mention HR and accounting dependencies explicitly.
- [ ] Call out policy or multi-company implications when relevant.

## Production readiness
- [ ] Identify the business entrypoint before tracing the flow.
- [ ] Trace downstream documents and approvals.
- [ ] Name cross-app bridges, accounting effects, and security or role implications.
- [ ] Keep implementation details out unless they change process meaning.

## Output
- [ ] Return base expense flow
- [ ] Return cross-app impacts
- [ ] Return roles and decision points
- [ ] Return golden-path test ideas
- [ ] Name assumptions, blockers, or missing context.
- [ ] Redirect clearly if the request crosses this skill boundary.
