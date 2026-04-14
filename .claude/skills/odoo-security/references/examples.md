# Examples

## Positive triggers
1. "Why can this employee see other expense sheets?"
   - Expected: use `odoo-security` as primary skill.
2. "Check public route and CSRF safety of this controller."
   - Expected: use `odoo-security` as primary skill.
3. "Review ACL and record-rule changes for this module."
   - Expected: use `odoo-security` as primary skill.

## Negative triggers
1. "What tests should run for this module?"
   - Expected: do not use `odoo-security` as primary skill.
2. "Explain the sales quotation process."
   - Expected: do not use `odoo-security` as primary skill.

## Tie-breaker
- Prompt: "Can portal users escalate access through this controller?"
- Why this skill wins: Permissions and exposure are central, so `odoo-security` should win over `odoo-review`.

## Nearby skills to consider
- `odoo-review`
- `odoo-build`
