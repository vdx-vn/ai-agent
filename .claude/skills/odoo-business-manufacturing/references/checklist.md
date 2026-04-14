# Checklist

## Intake
- [ ] Confirm the requested artifact belongs to `odoo-business-manufacturing`.
- [ ] Identify main module, bridge module, or business or technical entrypoint.
- [ ] Identify adjacent skills needed for composition.
- [ ] Identify nearest-neighbor skill and why it does not own the request.

## Analysis
- [ ] Identify BoM, MO, operation, or subcontracting entrypoint.
- [ ] Trace raw and finished moves into stock and valuation.
- [ ] Name bridge addons such as mrp_account, sale_mrp, or purchase_mrp.
- [ ] Call out quality, maintenance, or subassembly side effects when relevant.

## Production readiness
- [ ] Identify the business entrypoint before tracing the flow.
- [ ] Trace downstream documents and approvals.
- [ ] Name cross-app bridges, accounting effects, and security or role implications.
- [ ] Keep implementation details out unless they change process meaning.

## Output
- [ ] Return base manufacturing flow
- [ ] Return cross-app impacts
- [ ] Return roles and decision points
- [ ] Return golden-path test ideas
- [ ] Return boundary decision
- [ ] Name assumptions, blockers, or missing context.
- [ ] Redirect clearly if the request crosses this skill boundary.
