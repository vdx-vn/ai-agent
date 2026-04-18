# Examples

## Positive triggers
1. "What process and accounting steps happen after expense approval?"
   - Expected: use `odoo-business-expenses` as primary skill.
2. "How should employee-paid vs company-paid expenses differ?"
   - Expected: use `odoo-business-expenses` as primary skill.
3. "Which roles should approve and post this expense flow?"
   - Expected: use `odoo-business-expenses` as primary skill.

## Negative triggers
1. "How do contracts and attendances affect payroll prerequisites?"
   - Expected: do not use `odoo-business-expenses` as primary skill.
2. "What field type should this be?"
   - Expected: do not use `odoo-business-expenses` as primary skill.

## Tie-breaker
- Prompt: "How are employee-paid expenses reimbursed and posted?"
- Why this skill wins: The entrypoint is expense claim lifecycle, so `odoo-business-expenses` should win over `odoo-business-hr`.

## Nearby skills to consider
- `odoo-business-hr`
- `odoo-business-accounting`
- `odoo-security`
