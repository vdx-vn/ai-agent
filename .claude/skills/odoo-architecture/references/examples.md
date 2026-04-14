# Examples

## Positive triggers
1. "Should this logic live in sale, stock, or sale_stock?"
   - Expected: use `odoo-architecture` as primary skill.
2. "Do we need a bridge module or extend an existing addon?"
   - Expected: use `odoo-architecture` as primary skill.
3. "How should this addon depend on accounting and inventory?"
   - Expected: use `odoo-architecture` as primary skill.

## Negative triggers
1. "What ACL should this user have?"
   - Expected: do not use `odoo-architecture` as primary skill.
2. "How should this compute field depend list work?"
   - Expected: do not use `odoo-architecture` as primary skill.

## Tie-breaker
- Prompt: "Should this stock valuation hook live in stock_account or a new bridge addon?"
- Why this skill wins: This is fundamentally a placement and dependency decision, so `odoo-architecture` should win.

## Nearby skills to consider
- `odoo-plan`
- `odoo-build`
