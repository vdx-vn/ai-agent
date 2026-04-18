# Examples

## Positive triggers
1. "How do attendances and time off affect payroll prerequisites?"
   - Expected: use `odoo-business-hr` as primary skill.
2. "What HR apps are touched by custom contract approval?"
   - Expected: use `odoo-business-hr` as primary skill.
3. "What work-entry inputs should this change consider?"
   - Expected: use `odoo-business-hr` as primary skill.

## Negative triggers
1. "How are employee-paid expenses reimbursed?"
   - Expected: do not use `odoo-business-hr` as primary skill.
2. "Should this field be computed or stored?"
   - Expected: do not use `odoo-business-hr` as primary skill.

## Tie-breaker
- Prompt: "How do contracts and attendances affect payroll prerequisites?"
- Why this skill wins: The entrypoint is workforce and payroll prerequisite logic, so `odoo-business-hr` should win over `odoo-business-expenses`.

## Nearby skills to consider
- `odoo-business-timesheet-project-services`
- `odoo-business-expenses`
- `odoo-business-accounting`
