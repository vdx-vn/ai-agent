# Examples

## Positive triggers
1. "Should this be a search filter or kanban badge?"
   - Expected: use `odoo-view-ui` as primary skill.
2. "Add inherited form view with conditional group visibility."
   - Expected: use `odoo-view-ui` as primary skill.
3. "How should this action and menu be placed?"
   - Expected: use `odoo-view-ui` as primary skill.

## Negative triggers
1. "How should compute field dependencies work?"
   - Expected: do not use `odoo-view-ui` as primary skill.
2. "Why can this employee see all expense sheets?"
   - Expected: do not use `odoo-view-ui` as primary skill.

## Tie-breaker
- Prompt: "Should this action open a tree view first or a form view first?"
- Why this skill wins: The question is about UI behavior and action design, so `odoo-view-ui` should win.

## Nearby skills to consider
- `odoo-build`
- `odoo-business-website-ecommerce`
- `odoo-architecture`
