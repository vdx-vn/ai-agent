# Skill: Odoo Models & ORM

## Goal
Implement correct Odoo model logic using ORM patterns.

## Key Patterns
### create/write overrides
- Use `@api.model_create_multi` for create
- Always call super
- Avoid side effects unless necessary

### computed fields
- Use `compute='_compute_x'`
- Add `store=True` only when needed
- Provide inverse if field is editable

### onchange
- Only for UI experience, do not rely on it for business correctness

### constraints
- `@api.constrains(...)` for validation (server-side)
- Use `ValidationError`

### relational fields
- Many2one: ondelete should be meaningful
- One2many: never store business truth only in UI

## Guardrails
- Respect recordsets: methods should handle multi records unless ensure_one.
- Use `sudo()` sparingly; prefer proper rules.
- Avoid raw SQL unless performance-critical + reviewed.

## Example Prompt
"Add a computed margin field on sale.order.line and store it, update on price/qty changes."
