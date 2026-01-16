# Skill: Odoo Views / Actions / Menus

## Goal
Create/extend UI elements safely.

## Process
1) Determine view type: form/tree/kanban/search
2) Extend with inheritance:
   - `<field name="inherit_id" ref="..."/>`
   - Use xpath minimal + stable anchors
3) Action:
   - ir.actions.act_window for list/form
4) Menu:
   - Set parent and sequence
5) Add search filters + group by when useful
6) Odoo 18 not using 'states' anymore

## Guardrails
- Avoid fragile xpath (target on position by string)
- Ensure required fields are present or handle invisibility conditions
- Use `groups` attribute for restricted UI

## Example Prompt
"Add a smart button on partner to open related approvals."
