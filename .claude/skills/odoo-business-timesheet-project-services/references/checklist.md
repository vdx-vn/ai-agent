# Checklist

## Intake
- [ ] Confirm the requested artifact belongs to `odoo-business-timesheet-project-services`.
- [ ] Identify main module, bridge module, or business or technical entrypoint.
- [ ] Identify adjacent skills needed for composition.
- [ ] Identify nearest-neighbor skill and why it does not own the request.

## Analysis
- [ ] Identify service entrypoint: project, task, helpdesk, field service, or timesheet.
- [ ] Trace time capture to invoicing and analytics.
- [ ] Mention sale_project, hr_timesheet, or helpdesk links when relevant.
- [ ] Call out approval and billable or non-billable effects.

## Production readiness
- [ ] Identify the business entrypoint before tracing the flow.
- [ ] Trace downstream documents and approvals.
- [ ] Name cross-app bridges, accounting effects, and security or role implications.
- [ ] Keep implementation details out unless they change process meaning.

## Output
- [ ] Return base service flow
- [ ] Return cross-app impacts
- [ ] Return roles and decision points
- [ ] Return golden-path test ideas
- [ ] Return boundary decision
- [ ] Name assumptions, blockers, or missing context.
- [ ] Redirect clearly if the request crosses this skill boundary.
