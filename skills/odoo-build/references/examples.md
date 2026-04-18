# Examples

## Positive triggers
1. "Add approval field to expense sheet."
   - Expected: use `odoo-build` as primary skill.
2. "Implement stock validation rule in Odoo."
   - Expected: use `odoo-build` as primary skill.
3. "Create form view and access rights for this custom model."
   - Expected: use `odoo-build` as primary skill.

## Negative triggers
1. "Review whether this patch is safe before merge."
   - Expected: do not use `odoo-build` as primary skill.
2. "Compare two implementation options for this stock rule, no code yet."
   - Expected: do not use `odoo-build` as primary skill.

## Tie-breaker
- Prompt: "Add the computed margin field and update the form view."
- Why this skill wins: The user wants concrete changes produced in code and XML. `odoo-build` should win over `odoo-plan`.

## Nearby skills to consider
- `odoo-orm-modeling`
- `odoo-view-ui`
- `odoo-security`
- `odoo-upgrade-migration`
