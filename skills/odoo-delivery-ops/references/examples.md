# Examples

## Positive triggers
1. "What does -u vs --reinit mean for this rollout?"
   - Expected: use `odoo-delivery-ops` as primary skill.
2. "How should Odoo.sh staging and production branches work?"
   - Expected: use `odoo-delivery-ops` as primary skill.
3. "What runtime cautions matter for this module update?"
   - Expected: use `odoo-delivery-ops` as primary skill.

## Negative triggers
1. "How do I write migration script for this field rename?"
   - Expected: do not use `odoo-delivery-ops` as primary skill.
2. "How should a purchase order process work?"
   - Expected: do not use `odoo-delivery-ops` as primary skill.

## Tie-breaker
- Prompt: "What does `-u sale_stock` actually do on Odoo.sh staging?"
- Why this skill wins: The user wants command and environment mechanics, so `odoo-delivery-ops` should win over `odoo-ship`.

## Nearby skills to consider
- `odoo-ship`
- `odoo-test`
- `odoo-upgrade-migration`
