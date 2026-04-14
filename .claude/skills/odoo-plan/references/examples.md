# Examples

## Positive triggers
1. "Plan this purchase workflow customization."
   - Expected: use `odoo-plan` as primary skill.
2. "Give me step-by-step approach for this manufacturing feature."
   - Expected: use `odoo-plan` as primary skill.
3. "What files and tests should change for this stock rule?"
   - Expected: use `odoo-plan` as primary skill.

## Negative triggers
1. "What risks does this feature touch before we plan it?"
   - Expected: do not use `odoo-plan` as primary skill.
2. "Implement this stock rule now and update the XML."
   - Expected: do not use `odoo-plan` as primary skill.

## Tie-breaker
- Prompt: "Create implementation plan for portal invoice approval."
- Why this skill wins: The request clearly asks for ordered steps and delivery structure. `odoo-plan` should win over `odoo-think` and `odoo-build`.

## Nearby skills to consider
- `odoo-think`
- `odoo-test`
- `odoo-upgrade-migration`
