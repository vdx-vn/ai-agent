# Examples

## Positive triggers
1. "How do timesheets reach invoicing in service projects?"
   - Expected: use `odoo-business-timesheet-project-services` as primary skill.
2. "What apps are involved if tasks require billable approval?"
   - Expected: use `odoo-business-timesheet-project-services` as primary skill.
3. "Explain project and helpdesk link to service billing."
   - Expected: use `odoo-business-timesheet-project-services` as primary skill.

## Negative triggers
1. "How do transaction test tags work?"
   - Expected: do not use `odoo-business-timesheet-project-services` as primary skill.
2. "What worker config should Odoo.sh use?"
   - Expected: do not use `odoo-business-timesheet-project-services` as primary skill.

## Tie-breaker
- Prompt: "How does logged billable time reach invoicing in a service project?"
- Why this skill wins: The entrypoint is service delivery and billable time, so `odoo-business-timesheet-project-services` should win.

## Nearby skills to consider
- `odoo-business-sales`
- `odoo-business-hr`
- `odoo-business-accounting`
