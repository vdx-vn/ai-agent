# Examples

## Positive triggers
1. "What accounting entries change if stock valuation logic changes?"
   - Expected: use `odoo-business-accounting` as primary skill.
2. "How do taxes and fiscal positions affect this sales flow?"
   - Expected: use `odoo-business-accounting` as primary skill.
3. "What finance impact follows this expense approval change?"
   - Expected: use `odoo-business-accounting` as primary skill.

## Negative triggers
1. "Where should this code live, account or stock_account?"
   - Expected: do not use `odoo-business-accounting` as primary skill.
2. "How should this search view be arranged?"
   - Expected: do not use `odoo-business-accounting` as primary skill.

## Tie-breaker
- Prompt: "What finance impact follows changing stock valuation behavior?"
- Why this skill wins: The primary requested output is finance posting and valuation meaning, so `odoo-business-accounting` should win.

## Nearby skills to consider
- `odoo-business-sales`
- `odoo-business-purchase`
- `odoo-business-inventory`
- `odoo-business-expenses`
