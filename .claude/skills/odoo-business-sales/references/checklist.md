# Checklist

## Intake
- [ ] Confirm the requested artifact belongs to `odoo-business-sales`.
- [ ] Identify main module, bridge module, or business or technical entrypoint.
- [ ] Identify adjacent skills needed for composition.
- [ ] Identify nearest-neighbor skill and why it does not own the request.

## Analysis
- [ ] Identify entrypoint: lead, opportunity, quote, or backend order.
- [ ] Trace downstream logistics and invoicing documents.
- [ ] Name bridge modules such as sale_crm, sale_stock, or sale_project.
- [ ] Call out pricing, tax, delivery, or project side effects.

## Production readiness
- [ ] Identify the business entrypoint before tracing the flow.
- [ ] Trace downstream documents and approvals.
- [ ] Name cross-app bridges, accounting effects, and security or role implications.
- [ ] Keep implementation details out unless they change process meaning.

## Output
- [ ] Return base backend sales flow
- [ ] Return cross-app impacts
- [ ] Return roles and decision points
- [ ] Return golden-path test ideas
- [ ] Return boundary decision
- [ ] Name assumptions, blockers, or missing context.
- [ ] Redirect clearly if the request crosses this skill boundary.
