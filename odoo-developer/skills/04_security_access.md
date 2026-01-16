# Skill: Odoo Security Access

## Goal
Implement correct access control for models.

## Checklist
1) ACL: security/ir.model.access.csv
   - model_id, group_id, perm_read/write/create/unlink
2) Record Rules: security/security.xml
   - domain_force for row-level access
3) UI restriction:
   - groups on menu/actions/views/buttons
4) sudo():
   - only for system processes or controlled operations

## Guardrails
- Never rely on UI-only groups: must enforce in model/security too.
- For multi-company: use `company_id` and company rules properly.

## Example Prompt
"Only managers can delete approvals; users can only see their own requests."
