# Skill: Odoo Core Navigation

## Goal
Quickly locate the correct Odoo module/model/view and entry point.

## Inputs
- Feature description or bug report
- Model names (optional), UI screens (optional)
- Logs/traceback (optional)

## Output
- List of files to edit (models/views/security/data)
- Minimal change plan

## Process
1) Identify the functional area:
   - Sales: sale.order, sale.order.line
   - Purchase: purchase.order
   - Stock: stock.picking, stock.move
   - Accounting: account.move, account.payment
   - Product: product.template, product.product
2) Search patterns:
   - Model: `class Xxx(models.Model): _name = '...'`
   - Fields: `fields.*(`
   - Views: `<record id="..." model="ir.ui.view">`
   - Actions/Menu: `ir.actions.act_window`, `ir.ui.menu`
3) Confirm execution path:
   - UI create/write => model create/write overrides
   - Smart buttons => action methods
   - Cron => ir.cron, server actions => ir.actions.server

## Guardrails
- Prefer extending existing model methods rather than rewriting.
- Avoid editing core addons unless asked; use inheritance in custom module.

## Example Prompt
"Find where the 'Confirm' button in Sales Order triggers logic and how to add validation."
