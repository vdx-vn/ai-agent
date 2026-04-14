# Checklist

## Intake
- [ ] Confirm the requested artifact belongs to `odoo-business-inventory`.
- [ ] Identify main module, bridge module, or business or technical entrypoint.
- [ ] Identify adjacent skills needed for composition.

## Analysis
- [ ] Name the stock document type: receipt, delivery, internal transfer, adjustment, or valuation.
- [ ] Trace route and replenishment implications.
- [ ] Mention bridge addons such as sale_stock, purchase_stock, and stock_account.
- [ ] Call out valuation and traceability side effects.

## Production readiness
- [ ] Identify the business entrypoint before tracing the flow.
- [ ] Trace downstream documents and approvals.
- [ ] Name cross-app bridges, accounting effects, and security or role implications.
- [ ] Keep implementation details out unless they change process meaning.

## Output
- [ ] Return base warehouse or stock flow
- [ ] Return cross-app impacts
- [ ] Return roles and decision points
- [ ] Return golden-path test ideas
- [ ] Name assumptions, blockers, or missing context.
- [ ] Redirect clearly if the request crosses this skill boundary.
