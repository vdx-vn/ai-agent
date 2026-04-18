# Examples

## Positive triggers
1. "Help me scope this Odoo inventory customization."
   - Expected: use `odoo-think` as primary skill.
2. "What apps will this sale workflow change affect?"
   - Expected: use `odoo-think` as primary skill.
3. "Before coding, identify risks in this expense approval request."
   - Expected: use `odoo-think` as primary skill.

## Negative triggers
1. "Write step-by-step implementation plan for this module."
   - Expected: do not use `odoo-think` as primary skill.
2. "Review this diff for ACL mistakes."
   - Expected: do not use `odoo-think` as primary skill.

## Tie-breaker
- Prompt: "What could break if we change sale order confirmation?"
- Why this skill wins: The user wants risks and impact, not an ordered implementation plan. `odoo-think` should win over `odoo-plan`.

## Nearby skills to consider
- `odoo-plan`
- `odoo-architecture`
