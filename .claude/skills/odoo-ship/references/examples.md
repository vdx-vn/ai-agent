# Examples

## Positive triggers
1. "Prepare this Odoo change for release."
   - Expected: use `odoo-ship` as primary skill.
2. "What should we check before deploying this module?"
   - Expected: use `odoo-ship` as primary skill.
3. "Are we ready to ship this schema change?"
   - Expected: use `odoo-ship` as primary skill.

## Negative triggers
1. "Explain what -u does on Odoo.sh."
   - Expected: do not use `odoo-ship` as primary skill.
2. "Write migration script for renamed field."
   - Expected: do not use `odoo-ship` as primary skill.

## Tie-breaker
- Prompt: "Are we ready to deploy this schema change?"
- Why this skill wins: The user wants go or no-go readiness and rollout sequencing, not command semantics. `odoo-ship` should win over `odoo-delivery-ops` and compose with migration or test skills if evidence is still missing.

## Nearby skills to consider
- `odoo-delivery-ops`
- `odoo-upgrade-migration`
- `odoo-test`
