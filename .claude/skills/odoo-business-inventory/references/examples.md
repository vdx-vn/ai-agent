# Examples

## Positive triggers
1. "Explain route and replenishment impact of this warehouse change."
   - Expected: use `odoo-business-inventory` as primary skill.
2. "How do delivery, internal transfer, and valuation connect?"
   - Expected: use `odoo-business-inventory` as primary skill.
3. "What downstream effects follow a late stock move?"
   - Expected: use `odoo-business-inventory` as primary skill.

## Negative triggers
1. "How does a BoM shortage affect an MO?"
   - Expected: do not use `odoo-business-inventory` as primary skill.
2. "What tax report should accounting run?"
   - Expected: do not use `odoo-business-inventory` as primary skill.

## Tie-breaker
- Prompt: "How do replenishment rules create transfers and valuation changes?"
- Why this skill wins: The entrypoint is warehouse routing and stock documents, so `odoo-business-inventory` should win over `odoo-business-manufacturing`.

## Nearby skills to consider
- `odoo-business-sales`
- `odoo-business-purchase`
- `odoo-business-accounting`
- `odoo-business-manufacturing`
