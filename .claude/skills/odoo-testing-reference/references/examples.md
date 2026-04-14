# Examples

## Positive triggers
1. "When should I use HttpCase vs TransactionCase?"
   - Expected: use `odoo-testing-reference` as primary skill.
2. "How should I tag post-install tests?"
   - Expected: use `odoo-testing-reference` as primary skill.
3. "How do Odoo tours fit this workflow?"
   - Expected: use `odoo-testing-reference` as primary skill.

## Negative triggers
1. "Run validation for this change now."
   - Expected: do not use `odoo-testing-reference` as primary skill.
2. "Find security issues in this diff."
   - Expected: do not use `odoo-testing-reference` as primary skill.

## Tie-breaker
- Prompt: "Which Odoo test class should I use for checkout behavior?"
- Why this skill wins: This asks for framework choice, not current-change validation. `odoo-testing-reference` should win over `odoo-test`.

## Nearby skills to consider
- `odoo-test`
- `odoo-performance`
- `odoo-view-ui`
