# Examples

## Positive triggers
1. "Should this be a search filter or kanban badge?"
   - Expected: use `odoo-view-ui` as primary skill.
2. "Add inherited form view with conditional group visibility."
   - Expected: use `odoo-view-ui` as primary skill.
3. "Should this checkout template use xpath inheritance or a full QWeb override?"
   - Expected: use `odoo-view-ui` as primary skill.

## Negative triggers
1. "How does a shopper move from cart to order and delivery?"
   - Expected: do not use `odoo-view-ui` as primary skill.
2. "Why can this employee see all expense sheets?"
   - Expected: do not use `odoo-view-ui` as primary skill.

## Tie-breaker
- Prompt: "Should this website action open a tree view first or a form view first?"
- Why this skill wins: The request is about UI behavior and action mechanics, so `odoo-view-ui` should win over `odoo-business-website-ecommerce`.

## Nearby skills to consider
- `odoo-build`
- `odoo-business-website-ecommerce`
- `odoo-architecture`
