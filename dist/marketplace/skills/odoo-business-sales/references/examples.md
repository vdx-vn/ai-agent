# Examples

## Positive triggers
1. "Explain opportunity to quotation to invoice flow."
   - Expected: use `odoo-business-sales` as primary skill.
2. "What breaks if sale order confirms before stock availability check?"
   - Expected: use `odoo-business-sales` as primary skill.
3. "Which apps are touched by this custom sales approval?"
   - Expected: use `odoo-business-sales` as primary skill.

## Negative triggers
1. "How should compute field dependencies work?"
   - Expected: do not use `odoo-business-sales` as primary skill.
2. "What happens when a shopper checks out online?"
   - Expected: do not use `odoo-business-sales` as primary skill.

## Tie-breaker
- Prompt: "How does a salesperson convert an opportunity to a quotation and then an invoice?"
- Why this skill wins: The entrypoint is backend CRM and quotation workflow, so `odoo-business-sales` should win over `odoo-business-website-ecommerce`.

## Nearby skills to consider
- `odoo-business-inventory`
- `odoo-business-accounting`
- `odoo-business-website-ecommerce`
