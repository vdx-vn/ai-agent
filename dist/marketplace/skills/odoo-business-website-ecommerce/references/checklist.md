# Checklist

## Intake
- [ ] Confirm the requested artifact belongs to `odoo-business-website-ecommerce`.
- [ ] Identify main module, bridge module, or business or technical entrypoint.
- [ ] Identify adjacent skills needed for composition.
- [ ] Identify nearest-neighbor skill and why it does not own the request.

## Analysis
- [ ] Identify website entrypoint: public page, public form, shop, cart, checkout, or portal flow.
- [ ] Trace customer action into CRM, sales, stock, and payment flows.
- [ ] Mention website_sale, website_sale_stock, or website_crm.
- [ ] Call out public access and stock-visibility implications.

## Production readiness
- [ ] Identify the business entrypoint before tracing the flow.
- [ ] Trace downstream documents and approvals.
- [ ] Name cross-app bridges, accounting effects, and security or role implications.
- [ ] Keep template or xpath mechanics out unless they change process meaning.

## Output
- [ ] Return base website or ecommerce flow
- [ ] Return cross-app impacts
- [ ] Return roles and decision points
- [ ] Return golden-path test ideas
- [ ] Return boundary decision
- [ ] Name assumptions, blockers, or missing context.
- [ ] Redirect clearly if the request crosses this skill boundary.
