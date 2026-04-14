# Examples

## Positive triggers
1. "Test this stock customization."
   - Expected: use `odoo-test` as primary skill.
2. "What commands should I run to validate this module now?"
   - Expected: use `odoo-test` as primary skill.
3. "Check install and update regressions for this addon."
   - Expected: use `odoo-test` as primary skill.

## Negative triggers
1. "Explain Odoo test tags and HttpCase."
   - Expected: do not use `odoo-test` as primary skill.
2. "Review security rules in this patch."
   - Expected: do not use `odoo-test` as primary skill.

## Tie-breaker
- Prompt: "Validate this checkout change in install, update, and key workflows."
- Why this skill wins: The user wants current-change validation, not framework education. `odoo-test` should win over `odoo-testing-reference`.

## Nearby skills to consider
- `odoo-testing-reference`
- `odoo-performance`
