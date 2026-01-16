# Skill: Odoo Business Logic Workflows

## Goal
Implement state-based workflows (draft -> confirm -> done) safely.

## Patterns
- `state = fields.Selection([...], default='draft', tracking=True)`
- Transition methods:
  - `action_confirm`, `action_approve`, `action_done`, `action_cancel`
- Enforce correctness:
  - ValidationError on wrong transitions
- Use mail.thread for chatter when needed

## Guardrails
- Ensure concurrency safety when state changes affect accounting/stock
- Avoid partial updates: write state after required checks

## Example Prompt
"Add approval workflow for purchase orders with 2-step approvals."
