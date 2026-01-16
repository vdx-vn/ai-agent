# Skill: Odoo Testing & Quality

## Goal
Add tests for business-critical logic and prevent regressions.

## Tools
- `odoo.tests.common.TransactionCase`
- `SavepointCase` for speed
- Use demo data or create records in setup

## Must test
- Access rights
- State transitions
- Multi-company data separation
- Edge cases with empty recordsets

## Example Prompt
"Write tests for approval state transitions and access restrictions."
