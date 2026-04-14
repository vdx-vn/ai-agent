# Checklist

## Intake
- [ ] Confirm the requested artifact belongs to `odoo-business-purchase`.
- [ ] Identify main module, bridge module, or business or technical entrypoint.
- [ ] Identify adjacent skills needed for composition.

## Analysis
- [ ] Identify whether trigger is manual buying, replenishment, or MRP demand.
- [ ] Trace PO approval to pickings and bills.
- [ ] Name bridge modules such as purchase_stock or purchase_mrp.
- [ ] Call out stock, accounting, and approval side effects.

## Production readiness
- [ ] Identify the business entrypoint before tracing the flow.
- [ ] Trace downstream documents and approvals.
- [ ] Name cross-app bridges, accounting effects, and security or role implications.
- [ ] Keep implementation details out unless they change process meaning.

## Output
- [ ] Return base purchase flow
- [ ] Return cross-app impacts
- [ ] Return roles and decision points
- [ ] Return golden-path test ideas
- [ ] Name assumptions, blockers, or missing context.
- [ ] Redirect clearly if the request crosses this skill boundary.
