# Examples

## Positive triggers
1. "How does RFQ approval connect to receipts and vendor bills?"
   - Expected: use `odoo-business-purchase` as primary skill.
2. "Which apps are affected by custom PO approval?"
   - Expected: use `odoo-business-purchase` as primary skill.
3. "Explain replenishment-driven purchasing in Odoo."
   - Expected: use `odoo-business-purchase` as primary skill.

## Negative triggers
1. "What record rule should buyers have?"
   - Expected: do not use `odoo-business-purchase` as primary skill.
2. "Should this be a stored computed field?"
   - Expected: do not use `odoo-business-purchase` as primary skill.

## Tie-breaker
- Prompt: "How does an RFQ become a receipt and then a vendor bill?"
- Why this skill wins: The business entrypoint is buyer workflow, so `odoo-business-purchase` should win.

## Nearby skills to consider
- `odoo-business-inventory`
- `odoo-business-accounting`
- `odoo-business-manufacturing`
