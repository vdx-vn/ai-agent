# Examples

## Positive triggers
1. "Review this Odoo diff."
   - Expected: use `odoo-review` as primary skill.
2. "Check if this implementation follows Odoo best practice."
   - Expected: use `odoo-review` as primary skill.
3. "Find risks in this customization before merge."
   - Expected: use `odoo-review` as primary skill.

## Negative triggers
1. "Run install and update validation for this addon now."
   - Expected: do not use `odoo-review` as primary skill.
2. "Plan this feature from zero."
   - Expected: do not use `odoo-review` as primary skill.

## Tie-breaker
- Prompt: "Inspect this diff for likely regressions before merge."
- Why this skill wins: The user wants findings on an existing artifact, not executed validation evidence. `odoo-review` should win over `odoo-test`.

## Nearby skills to consider
- `odoo-security`
- `odoo-test`
- `odoo-testing-reference`
