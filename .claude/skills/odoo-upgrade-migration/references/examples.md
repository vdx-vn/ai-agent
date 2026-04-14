# Examples

## Positive triggers
1. "How do I rename this field and preserve data?"
   - Expected: use `odoo-upgrade-migration` as primary skill.
2. "Do we need a migration for moving data to a new addon?"
   - Expected: use `odoo-upgrade-migration` as primary skill.
3. "What should upgrade script phases look like here?"
   - Expected: use `odoo-upgrade-migration` as primary skill.

## Negative triggers
1. "What worker config should production use?"
   - Expected: do not use `odoo-upgrade-migration` as primary skill.
2. "Explain website cart flow."
   - Expected: do not use `odoo-upgrade-migration` as primary skill.

## Tie-breaker
- Prompt: "How should we deploy a renamed invoice field with existing data preserved?"
- Why this skill wins: Data preservation and schema transition are central, so `odoo-upgrade-migration` should win over `odoo-delivery-ops`.

## Nearby skills to consider
- `odoo-ship`
- `odoo-plan`
- `odoo-delivery-ops`
