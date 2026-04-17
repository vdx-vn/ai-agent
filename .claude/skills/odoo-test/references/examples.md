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
2. "Review this diff for maintainability and risk before merge."
   - Expected: do not use `odoo-test` as primary skill.

## Tie-breaker
- Prompt: "Validate this checkout change in install, update, and key workflows."
- Why this skill wins: The user wants current-change validation evidence, not framework education or review findings. `odoo-test` should win over `odoo-testing-reference` and `odoo-review`.

## Nearby skills to consider
- `odoo-review`
- `odoo-testing-reference`
- `odoo-performance`
- `odoo-local-test-harness`
