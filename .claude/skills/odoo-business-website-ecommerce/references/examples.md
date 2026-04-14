# Examples

## Positive triggers
1. "What is flow from website cart to sales order to delivery?"
   - Expected: use `odoo-business-website-ecommerce` as primary skill.
2. "How does stock visibility affect shop behavior?"
   - Expected: use `odoo-business-website-ecommerce` as primary skill.
3. "How are website forms turned into leads or orders?"
   - Expected: use `odoo-business-website-ecommerce` as primary skill.

## Negative triggers
1. "How does a salesperson convert opportunity to quotation?"
   - Expected: do not use `odoo-business-website-ecommerce` as primary skill.
2. "Should this checkout template use xpath inheritance or a full QWeb override?"
   - Expected: do not use `odoo-business-website-ecommerce` as primary skill.

## Tie-breaker
- Prompt: "What happens when a shopper checks out with an out-of-stock item?"
- Why this skill wins: The entrypoint is cart and checkout behavior in the public customer journey, so `odoo-business-website-ecommerce` should win over `odoo-business-sales` and `odoo-view-ui`.

## Nearby skills to consider
- `odoo-business-sales`
- `odoo-business-inventory`
- `odoo-view-ui`
- `odoo-security`
