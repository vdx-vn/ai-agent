# Examples

## Positive triggers
1. "Design webhook sync from external WMS to Odoo."
   - Expected: use `odoo-integration-api` as primary skill.
2. "Should this integration use a bot user or an employee account?"
   - Expected: use `odoo-integration-api` as primary skill.
3. "What API approach fits this partner-system sync?"
   - Expected: use `odoo-integration-api` as primary skill.

## Negative triggers
1. "How do I design this form view?"
   - Expected: do not use `odoo-integration-api` as primary skill.
2. "Which module should own this compute field?"
   - Expected: do not use `odoo-integration-api` as primary skill.

## Tie-breaker
- Prompt: "Should we sync warehouse receipts with XML-RPC or a custom HTTP endpoint?"
- Why this skill wins: The primary decision is external integration contract and auth model, so `odoo-integration-api` should win.

## Nearby skills to consider
- `odoo-security`
- `odoo-delivery-ops`
- `odoo-build`
